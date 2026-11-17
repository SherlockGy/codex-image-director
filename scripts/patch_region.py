# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pillow",
# ]
# ///
"""局部贴回：以旧图为底，只把新图指定区域的像素贴回，其余像素保持不变。

用于编辑模式下目标区域改对了、但别处也跟着变了的情况。
用法见 `uv run patch_region.py -h`。
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

# 放大核对图的放大倍数
ZOOM_FACTOR = 3
# 放大核对图在改动外框四周额外保留的像素
ZOOM_MARGIN = 40


def parse_numbers(text: str, count: int, label: str) -> tuple[int, ...]:
    """把 '1,2,3,4' 解析成整数元组，数量不对时报错。"""
    try:
        values = tuple(int(v.strip()) for v in text.split(","))
    except ValueError:
        raise argparse.ArgumentTypeError(f"{label} 需要 {count} 个整数，用逗号分隔：{text!r}")
    if len(values) != count:
        raise argparse.ArgumentTypeError(f"{label} 需要 {count} 个整数，实际 {len(values)} 个：{text!r}")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="以旧图为底，只贴回新图的指定区域。")
    parser.add_argument("--base", required=True, type=Path, help="旧图（底），其余像素保持不变")
    parser.add_argument("--source", required=True, type=Path, help="新图（编辑后的图），只取指定区域")
    parser.add_argument("--out", required=True, type=Path, help="输出路径；已存在时拒绝覆盖")
    parser.add_argument(
        "--ellipse", action="append", default=[], type=lambda t: parse_numbers(t, 4, "--ellipse"),
        help="椭圆区域 cx,cy,rx,ry（像素，以底图为准）；可重复",
    )
    parser.add_argument(
        "--rect", action="append", default=[], type=lambda t: parse_numbers(t, 4, "--rect"),
        help="矩形区域 x1,y1,x2,y2（像素，以底图为准）；可重复",
    )
    parser.add_argument("--feather", type=int, default=3, help="边缘羽化半径（像素），默认 3")
    parser.add_argument(
        "--resize-source", action="store_true",
        help="两图尺寸不同时把新图缩放到底图尺寸；只有确认构图一致时才使用",
    )
    parser.add_argument("--zoom", type=Path, help="可选：输出改动区域的放大核对图")
    return parser.parse_args()


def validate(args: argparse.Namespace, size: tuple[int, int]) -> list[str]:
    """校验区域、羽化和输出路径，返回错误列表。"""
    errors = []
    width, height = size

    if not args.ellipse and not args.rect:
        errors.append("至少需要一个 --ellipse 或 --rect 区域")

    if args.feather < 0:
        errors.append("--feather 不能为负数")

    for cx, cy, rx, ry in args.ellipse:
        if rx <= 0 or ry <= 0:
            errors.append(f"椭圆半径必须为正：{cx},{cy},{rx},{ry}")
        if not (0 <= cx < width and 0 <= cy < height):
            errors.append(f"椭圆中心超出图片范围 {width}x{height}：{cx},{cy}")

    for x1, y1, x2, y2 in args.rect:
        if x1 >= x2 or y1 >= y2:
            errors.append(f"矩形需要 x1<x2 且 y1<y2：{x1},{y1},{x2},{y2}")
        if x1 < 0 or y1 < 0 or x2 > width or y2 > height:
            errors.append(f"矩形超出图片范围 {width}x{height}：{x1},{y1},{x2},{y2}")

    if args.out.exists():
        errors.append(f"输出文件已存在，拒绝覆盖：{args.out}")

    return errors


def main() -> int:
    args = parse_args()

    # 统一日志前缀，便于区分每次贴回
    log_prefix = f"[patch_region 局部贴回][out={args.out.name}]"

    for label, path in (("--base", args.base), ("--source", args.source)):
        if not path.is_file():
            print(f"{log_prefix} 参数错误：{label} 文件不存在：{path}", file=sys.stderr)
            return 2

    base = Image.open(args.base).convert("RGB")
    source = Image.open(args.source).convert("RGB")

    # 尺寸不同意味着像素无法一一对应，默认拒绝，避免错位贴回
    if source.size != base.size:
        if not args.resize_source:
            print(
                f"{log_prefix} 参数错误：两图尺寸不同（底图 {base.size}，新图 {source.size}）。"
                "确认构图一致后可加 --resize-source",
                file=sys.stderr,
            )
            return 2
        print(f"{log_prefix} 注意：新图从 {source.size} 缩放到 {base.size}，可能有轻微错位", flush=True)
        source = source.resize(base.size, Image.LANCZOS)

    errors = validate(args, base.size)
    if errors:
        for error in errors:
            print(f"{log_prefix} 参数错误：{error}", file=sys.stderr)
        return 2

    # 构建羽化遮罩：白色区域取新图，黑色区域保留旧图
    mask = Image.new("L", base.size, 0)
    draw = ImageDraw.Draw(mask)
    for cx, cy, rx, ry in args.ellipse:
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
    for x1, y1, x2, y2 in args.rect:
        draw.rectangle([x1, y1, x2, y2], fill=255)
    if args.feather:
        mask = mask.filter(ImageFilter.GaussianBlur(args.feather))

    result = Image.composite(source, base, mask)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    result.save(args.out)

    # 改动外框必须只落在目标区域内，用来核对没有误改别处
    bbox = ImageChops.difference(base, result).getbbox()
    print(f"{log_prefix} 完成，输出={args.out}，改动外框={bbox}", flush=True)

    if args.zoom and bbox:
        x1, y1, x2, y2 = bbox
        crop_box = (
            max(0, x1 - ZOOM_MARGIN), max(0, y1 - ZOOM_MARGIN),
            min(base.width, x2 + ZOOM_MARGIN), min(base.height, y2 + ZOOM_MARGIN),
        )
        crop = result.crop(crop_box)
        crop = crop.resize((crop.width * ZOOM_FACTOR, crop.height * ZOOM_FACTOR), Image.LANCZOS)
        args.zoom.parent.mkdir(parents=True, exist_ok=True)
        crop.save(args.zoom)
        print(f"{log_prefix} 放大核对图={args.zoom}", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
