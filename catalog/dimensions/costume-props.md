# 服装、道具与材质

## 服装的描述顺序

从上到下逐件写，每件写清轮廓、材质、颜色、细节和计数，最后写禁止项：

```text
上衣（领型 / 袖型 / 开口 / 材质 / 透明度）→ 腰部 → 下装（长度 / 褶数与朝向 / 开衩）→ 腿（袜：颜色写死）→ 鞋（鞋型 / 跟高 / 材质 / 系带）
→ 配饰（位置 / 尺寸 / 计数 / 状态）→ Forbidden：<不许出现的>
```

- 计数和朝向写成：at least twenty narrow knife pleats, all folding in the same direction；exactly three separate strokes that do not touch。
- 不许出现的东西要明确写：nothing hangs from the waist；no metal or jewel on the bow；sleeves never rolled up。

## 从设定图换装

- 设定图是平面线稿或插画时，写：take ONLY the design (form, costume, accessories), NOT their 2D drawing style。
- 有三视图时，指定以哪张为准：authoritative for costume details。
- 新服装和动作冲突时（拖地长裙配高抬腿等），先在提示词里给出解法，例如 one long leg emerges from the high skirt slit。

## 道具

写清形态、材质、相对尺度，以及“没有什么”：

- 尺度用身体做单位：about as wide as two of her fingers；about one head length long。
- 排除误读：it is not a creature, not a bulb, not a sticker。
- 动作不合常理时，写明道具没有辅助结构：has NO pedal, NO stirrup, NO footrest。

## 易画性改造

| 难画的形态 | 改法 | 写法示例 |
|---|---|---|
| 又细又长的直物 | 加粗、加贯穿全长的棱边、加等距标记、缩短 | a long slim perfectly straight prism with a rhombic cross-section, four crisp edges running its full length；evenly spaced collar rings；moderate length |
| 两段汇于一点的线 | 定义唯一交点 | both halves meet at exactly ONE point … forming a clean V with its apex at <位置>; each half one perfectly straight taut line |
| 对称结构画歪 | 写对称和干净的轮廓 | crisp symmetrical limbs with a clean silhouette, no wavy, melted or snake-like distortion |
| 精确计数的小物 | 写 exactly N，并逐个描述 | (1) one large open arc … (2) … (3) … |
| 纯能量物体 | 给它几何边界和内部结构，避免一团糊光 | pure condensed light with crisp faceted edges glowing brighter, a bright core line through the center |

## 材质

| 材质 | 写法 | 注意 |
|---|---|---|
| 漆皮 | glossy patent leather with realistic specular highlights and reflections | 镜头太远时看不出质感，要配合景别 |
| 金属 | polished / brushed silver with micro-scratches and soft reflections | — |
| 丝袜 | sheer nylon with realistic denier transparency；写明颜色 | 只写 low denier 容易发棕，要写颜色并排除棕色 |
| 丝绸、薄纱 | real silk and chiffon with soft physical folds and translucency | — |
| 宝石、玻璃 | clear amber glass, faceted crystal accents | — |

## 派生设计（从已有元素演变出新物件）

- 基因不变，形态重组：保留源头的辨识特征（颜色、光感、标志线条），重组成目标品类自己的形态。
- 第一眼是目标品类，细看才发现同源：It reads first as <品类>, and only on a closer look <关联>。
- 把源头原样缩小后贴上去，不算派生设计。
- 写“像 X 一样”的比喻，容易被画成 X 本身。直接写形状和材质。

## 常见失败与对策

| 现象 | 对策 |
|---|---|
| 材质词自带默认颜色，导致颜色漂移 | 写颜色，并排除漂移色 |
| 细长物画弯 | 走易画性改造，不要只加 straight |
| 道具上多出结构 | 写 has NO … |
| 计数漂移，多一笔或少一颗 | exactly N 加逐个描述；验收时放大核对 |
| 换装后旧服装元素残留 | Avoid 里点名旧服装的元素 |
| 服装被模型悄悄改了（裙子变短等） | 预判冲突，在提示词里给出解法；交付时说明偏差 |
