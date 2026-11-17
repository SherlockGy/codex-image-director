#!/usr/bin/env python
"""通过本机 Codex CLI 调用内置 image_gen 生成或编辑一张图，并按版本号保存到输出目录。

只用 Python 3.10+ 标准库，可直接 `python gen.py ...` 运行。
用法见 `python gen.py -h`。
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Codex 内置生图的默认落盘目录：$CODEX_HOME/generated_images/<thread_id>/
CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
GENERATED_DIR = CODEX_HOME / "generated_images"

# 单次生图最长等待秒数；超时视为失败，避免进程挂住
TIMEOUT_SECONDS = 900

# 认作图片的扩展名：用于校验输入图片和查找生成产物
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}

# 包装语：要求 Codex 原样调用一次 image_gen，不改写、不自查重画、不做其他事
WRAPPER = (
    "Call the built-in image_gen tool exactly once using the image prompt below, verbatim. "
    "Any attached images are inputs exactly as the prompt describes (edit target or references). "
    "Do not write code, do not run shell commands, do not edit files, and do not ask questions. "
    "After the tool returns, reply with the single word DONE.\n\n"
    "<image_prompt>\n{image_prompt}\n</image_prompt>\n"
)


def build_image_prompt(spec_files: list[Path], prompt_file: Path) -> str:
    """拼接最终图像提示词：固定设定文件（可多个，按顺序）+ 本图规格。"""
    # utf-8-sig 兼容 Windows 编辑器写入的 BOM，避免 BOM 字符混进提示词
    parts = [p.read_text(encoding="utf-8-sig").strip() for p in spec_files]
    parts.append(prompt_file.read_text(encoding="utf-8-sig").strip())
    return "\n\n".join(part for part in parts if part)


def next_version_stem(out_dir: Path, name: str) -> str:
    """返回下一个未被占用的版本名（不含扩展名），如 hero-v002；任何扩展名的同版本文件都算占用。"""
    version = 1
    while True:
        stem = f"{name}-v{version:03d}"
        # 名字里可能有 [ ] 等通配字符，先转义再匹配
        if not any(out_dir.glob(f"{glob.escape(stem)}.*")):
            return stem
        version += 1


def find_thread_id(stdout: str) -> str | None:
    """从 codex --json 事件流里取会话 id，生成图在同名目录下。"""
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "thread.started":
            return event.get("thread_id")
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="通过 Codex CLI 内置 image_gen 生成或编辑一张图，按版本号保存。",
    )
    parser.add_argument("--prompt", required=True, type=Path, help="本图规格提示词文件（UTF-8）")
    parser.add_argument("--name", required=True, help="产物名，输出为 <name>-vNNN.<扩展名>；不能含路径分隔符")
    parser.add_argument("--out-dir", required=True, type=Path, help="输出目录，不存在时自动创建")
    parser.add_argument(
        "--spec", action="append", default=[], type=Path,
        help="固定设定文件，拼接在本图规格之前；可重复，按出现顺序拼接；编辑类任务不要使用",
    )
    parser.add_argument(
        "--ref", action="append", default=[], type=Path,
        help="输入图片，可重复；顺序对应提示词里的 Image 1、Image 2……；编辑任务的底图必须放第一个",
    )
    parser.add_argument("--dry-run", action="store_true", help="只打印拼装结果和命令，不调用 Codex、不消耗额度")
    return parser.parse_args()


def validate(args: argparse.Namespace) -> list[str]:
    """在任何调用之前校验输入，返回错误列表。"""
    errors = []

    # 产物名只能是文件名，避免写到输出目录以外
    if not args.name or Path(args.name).name != args.name or args.name in (".", ".."):
        errors.append(f"--name 只能是文件名，不能包含路径：{args.name!r}")

    for label, paths in (("--prompt", [args.prompt]), ("--spec", args.spec), ("--ref", args.ref)):
        for path in paths:
            if not path.is_file():
                errors.append(f"{label} 文件不存在：{path}")

    # 输入图片必须是常见图片格式，避免误把提示词文件当图片传入
    for ref in args.ref:
        if ref.suffix.lower() not in IMAGE_SUFFIXES:
            errors.append(f"--ref 不是支持的图片格式（{'/'.join(sorted(IMAGE_SUFFIXES))}）：{ref}")

    # 同一个文件重复传入通常是笔误，会让 Image 编号错位
    resolved_refs = [str(p.resolve()) for p in args.ref]
    if len(resolved_refs) != len(set(resolved_refs)):
        errors.append("--ref 中有重复的图片，会让 Image 编号错位")

    if args.out_dir.exists() and not args.out_dir.is_dir():
        errors.append(f"--out-dir 不是目录：{args.out_dir}")

    return errors


def main() -> int:
    args = parse_args()

    # 统一日志前缀，便于并行生成时区分每张图
    log_prefix = f"[gen 生成图片][name={args.name}]"

    errors = validate(args)
    if errors:
        for error in errors:
            print(f"{log_prefix} 参数错误：{error}", file=sys.stderr)
        return 2

    image_prompt = build_image_prompt(args.spec, args.prompt)
    codex_input = WRAPPER.format(image_prompt=image_prompt)

    # Windows 下优先用 npm 生成的 codex.cmd，避开 PowerShell 执行策略对 codex.ps1 的拦截
    codex = shutil.which("codex.cmd") or shutil.which("codex")
    out_dir = args.out_dir.resolve()
    # 只读沙箱：Codex 只负责调用生图，不写任何文件；产物由本脚本复制
    command = [codex or "codex", "exec", "--skip-git-repo-check", "-s", "read-only", "--json", "-C", str(out_dir)]
    for ref in args.ref:
        command += ["-i", str(ref.resolve())]

    if args.dry_run:
        print(f"{log_prefix} 预演模式，不调用 Codex")
        print(f"{log_prefix} 命令：{' '.join(command)}")
        for index, ref in enumerate(args.ref, start=1):
            print(f"{log_prefix} Image {index} = {ref}")
        print(f"{log_prefix} 发送给 Codex 的内容如下：\n{codex_input}")
        return 0

    if not codex:
        print(f"{log_prefix} 失败：找不到 codex 命令，请确认 Codex CLI 已安装并在 PATH 中", file=sys.stderr)
        return 1

    # codex 的 -C 工作目录必须存在，真正调用前才创建输出目录
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"{log_prefix} 开始调用 codex，输入图片数量={len(args.ref)}", flush=True)
    try:
        result = subprocess.run(
            command, input=codex_input, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        print(f"{log_prefix} 失败：超过 {TIMEOUT_SECONDS} 秒未完成。请检查是否残留 codex 进程", file=sys.stderr)
        return 1

    thread_id = find_thread_id(result.stdout)
    images = []
    if thread_id:
        thread_dir = GENERATED_DIR / thread_id
        images = sorted(
            (p for p in thread_dir.glob("*") if p.suffix.lower() in IMAGE_SUFFIXES),
            key=lambda p: p.stat().st_mtime,
        )

    if not images:
        print(f"{log_prefix} 失败：未找到生成图，退出码={result.returncode}，thread={thread_id}", file=sys.stderr)
        print(result.stdout[-1500:], file=sys.stderr)
        print(result.stderr[-1500:], file=sys.stderr)
        return 1

    # 取本会话最新的一张，保留原扩展名；同时保存实际发送的提示词，便于追溯和复现
    source = images[-1]
    stem = next_version_stem(out_dir, args.name)
    target = out_dir / f"{stem}{source.suffix.lower()}"
    shutil.copy2(source, target)
    record = out_dir / f"{stem}.prompt.txt"
    ref_lines = "\n".join(f"Image {i} = {p.resolve()}" for i, p in enumerate(args.ref, start=1)) or "(无输入图片)"
    record.write_text(f"{ref_lines}\n\n{image_prompt}\n", encoding="utf-8")

    if len(images) > 1:
        print(f"{log_prefix} 注意：本会话生成了 {len(images)} 张图，只复制了最新一张；其余在 {GENERATED_DIR / thread_id}", flush=True)
    print(f"{log_prefix} 完成，thread={thread_id}，输出={target}，提示词记录={record}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
