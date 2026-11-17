# 提示词语言与结构

## 语言

- 提示词用英文。镜头、材质、人体、渲染这类专业词，英文更准确。
- 用户的中文反馈先**复述确认**，再翻译成可验证的英文约束：
  - “自然一点”：写清具体哪里、怎么样。例如 index finger straight, other fingers softly curled。
  - “更有冲击力”：翻译成镜头、动势、特效等手段（见 camera 卡）。
  - “一样长”“对齐”：翻译成几何约束。

## 结构

用标签行分段，按需取用，不留空标签：

```text
Use case / Asset type / Input images / Style/medium / Rendering rules / Subject / Props / Scene /
Framing / Pose and interaction / Geometry / Expression / Motion / Lighting / Physics / Avoid
系列项目额外可用：State / World
```

- 顺序：先定是什么图、用什么参考，再写画风，然后是主体、环境、镜头、动作，最后写约束和排除。
- 长度：规格详细不是问题。Codex 自己的生图规则对已经具体的提示词只做规范化，不扩写；真正的风险是被改写，所以要用下面的包装语。
- `Use case` 用 Codex 生图规则里的分类名，帮助它判断这是生成还是编辑：
  - 生成：stylized-concept（风格化、3D 渲染）、photorealistic-natural（照片写实）、illustration-story（叙事插画）、product-mockup、ui-mockup、infographic-diagram 等。
  - 编辑：precise-object-edit（局部改动）、identity-preserve（锁定人物换其他）、style-transfer（换画风）、lighting-weather、compositing 等。
- 画幅比例写在 Asset type 行，例如 16:9 landscape, full-bleed。内置生图工具没有尺寸或质量参数。

## Codex 包装语（`scripts/gen.py` 已内置）

```text
Call the built-in image_gen tool exactly once using the image prompt below, verbatim.
Any attached images are inputs exactly as the prompt describes (edit target or references).
Do not write code, do not run shell commands, do not edit files, and do not ask questions.
After the tool returns, reply with the single word DONE.
```

- 原因：Codex 收到任务后会先读自己的 imagegen 规则，再按规则重写提示词，还可能自查后重画。
- 原样包装能减少改写，避免额外消耗额度；验收由 agent 自己完成。

## 用词规则

| 规则 | 正例 | 反例 |
|---|---|---|
| 物体尺寸用身体或常见物做单位 | about two fingers wide；one and a half shoe lengths apart | about 5% of the frame（描述物体大小时不稳定；画面占比可以用百分比） |
| 计数写死 | exactly three；at least twenty, all folding the same direction | several, some |
| 程度加排除 | only very slightly … never annoyed | slightly frowning |
| 只写形状，不用比喻 | a soft pear-shaped glow tapering into one curling wisp | like a little heart |
| 写“没有什么” | has NO pedal；nothing hangs from the waist | （不写，模型会自己补） |
| 几何写成可验证的约束 | meet at exactly ONE point；each segment perfectly straight | make the string look right |
| 接触关系写清楚 | with a clear small gap of air；the hand does not touch the arrow | near the arrow |
| 参考图按编号写职责 | Image 2: take only the pose. Do NOT take her outfit | use image 2 as reference |

## Avoid 行

- 只写针对本图风险的项：相邻写实档、已知漂移（颜色、形状）、多余结构、裁切、文字水印、参考图里不要的元素。
- 不要堆砌通用的长清单，它会稀释真正关键的排除项。
- 每张图都带上：extra limbs, extra fingers, text, watermark。

## 编辑固定句

```text
Edit: change only <X>. It currently <现在的错>. Make it <目标>.
Keep everything else exactly unchanged: same <逐项>, framing, lighting and aspect ratio.
Do not redraw or restyle anything else. No text, no watermark.
```

## 参考图固定句

```text
Image 1 is <角色>: match her face, hair, outfit and rendering exactly. Do not reproduce its layout, pose or background.
Image 2 is a reference for <局部> only. Ignore its rendering style, its scale and its background.
Image 3: take ONLY the design, NOT its drawing style.
```
