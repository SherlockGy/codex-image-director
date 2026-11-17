# 画面维度知识卡索引

> 维度卡用来查写法：要决定什么、哪些词有效、常见失败和对策。执行步骤、命令和验收都写在 `flows/` 的流程文件里，维度卡不承载执行流程。

## 选卡规则

| 当前流程 / 档位 | 读哪些卡 |
|---|---|
| 单张·快速档 | camera-composition、style-realism、prompt-language |
| 单张·精品档、系列项目写固定设定时、改造已有图 | 全部 7 张 |
| 系列项目写场景卡 | camera-composition、body-pose-hands、light-environment-physics、prompt-language |
| 方案探索 | costume-props（含派生设计）、prompt-language |
| 精修已有图 | 改动涉及的那一张 + prompt-language |

选定后回复：“读维度卡 <卡名…>，依据：本图涉及 <维度>”。

## 卡片

| 维度 | 卡片 | 什么时候查 |
|---|---|---|
| 镜头、机位、构图、透视、占比、留白 | [dimensions/camera-composition.md](dimensions/camera-composition.md) | 定画面骨架；要冲击力；要转镜头或挪主体 |
| 身体、动作受力、肢体比例、手 | [dimensions/body-pose-hands.md](dimensions/body-pose-hands.md) | 有动作；有手部持握；肢体透视缩短 |
| 面部、眼睛、表情、年龄感 | [dimensions/face-expression.md](dimensions/face-expression.md) | 写角色脸；要保住脸；表情要有分寸 |
| 服装、道具、材质、派生设计 | [dimensions/costume-props.md](dimensions/costume-props.md) | 写服装或道具；道具难画；从设定图换装 |
| 光影、环境层次、物理规则、特效 | [dimensions/light-environment-physics.md](dimensions/light-environment-physics.md) | 写光和背景；背景太空或太挤；有能量特效 |
| 写实刻度与画风 | [dimensions/style-realism.md](dimensions/style-realism.md) | 定画风；用户说“太假”或“写实过头了” |
| 提示词语言、结构、用词规则、Codex 包装 | [dimensions/prompt-language.md](dimensions/prompt-language.md) | 每次写提示词 |

## 维护说明

新增卡片或改名时，同步本表、`SKILL.md` 中的链路说明，以及各流程里引用卡片的位置。
