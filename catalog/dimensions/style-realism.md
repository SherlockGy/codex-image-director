# 写实刻度与画风

## 刻度

写实程度是连续的，一个词定不住位置。先定档，再用锚定词钉住，同时排除相邻两档。

| 档 | 名称 | 锚定词（英文） | 常见误入 |
|---|---|---|---|
| 1 | 平面插画 | flat 2D illustration, clean line art, cel shading | — |
| 2 | 二次元风格化 3D（卡通渲染） | real-time toon-shaded 3D (NPR), crisp two-tone shadow shapes, fine inverted-hull outlines, volumetric hair clumps casting shadows on the face, ambient occlusion in folds, a 3D model with a hand-painted anime look | 写“3D”却没写 toon 规则，容易变成欧美 3D 动画脸 |
| 3 | 2.5D 精修插画 | painterly digital illustration with 3D-like lighting | 实践中出现过：只写“3D 超写实”配奇幻题材，落到了这一档；发光的头发和纱料是这一档的标志 |
| 4 | 理想化写实（CG 角色走进现实） | idealized refined hyper-realism, a top-tier game CG heroine brought into the real world, flawless smooth luminous porcelain skin, soft subsurface scattering, only a very subtle micro-texture, no visible pores, silky realistic hair strands, real fabric physics, controlled bloom | 加了 pores、film grain 会滑到第 5 档 |
| 5 | 电影级写实 CG | path-traced cinematic CG, visible fine pores, natural specular, real camera lens, film grain | 实践中曾被用户评价为“写实过头” |
| 6 | 照片写实 | photorealistic, real-world texture, natural imperfections | — |

## 写法

```text
Style/medium: <第 N 档锚定词>.
Rendering rules:
- Skin: <本档皮肤>
- Hair: <本档头发>
- Materials: <本档材质>
- Lighting: <本档光>
Avoid: <第 N-1 档的特征>, <第 N+1 档的特征>
```

- 第 4 档的排除项：2D, anime line art, painterly illustration, gritty skin pores, aged or rough skin, documentary photo look。
- 第 2 档的排除项：Disney or Pixar look, Western 3D animation, realistic human face, plastic skin, flat 2D illustration without volume。

## 规则

- 描述渲染技术特征，不写作品名、游戏名、工作室名。作品名没有被证明更有效，还会带来版权风险和不可控的联想。
- 质量标签（masterpiece、8k、best quality）没有证据证明有效，不依赖它们。
- 用户说“太假”或“写实过头”时，先判断现在落在哪一档、目标是哪一档，再改锚定词和排除项，不要只加或减一个词。
- 在原图上用编辑模式做大跨度的刻度调整（例如从第 3 档调到第 4 档），模型为了保住脸和服装，往往改不动。这时向用户说明，并给出“以当前图为参考重新生成”的选项和代价。

## 常见失败与对策

| 现象 | 对策 |
|---|---|
| 单写“3D 超写实”，结果出来插画感 | 换成第 4 档全套锚定词，并排除第 3 档 |
| 加了毛孔、胶片颗粒，变成粗糙的真人照 | 回到第 4 档，写 no visible pores，并排除 gritty |
| 卡通渲染变成欧美 3D 动画脸 | 写日系脸部结构（见 face 卡），并排除 Western 3D animation |
| 编辑后刻度变化很小 | 说明编辑的局限，提供重生成选项 |
