# 标定记分卡 v1

## 一、第 1 轮：与人工基准对照（13 条）

| 轴 | 审计员 A | 审计员 B | A 与 B 一致性 |
|---|---|---|---|
| 支撑（SUPPORTED/PARTIAL/UNSUPPORTED） | 11 / 13 | 11 / 13 | **13 / 13** |
| 自足（SELF/DEPENDENT） | 13 / 13 | 10 / 13 | 10 / 13 |

**支撑轴的两处不一致，A 和 B 落在同两条上、朝同一方向（都比我严）**：

| id | 我的基准 | A | B | 性质 |
|---|---|---|---|---|
| 02 | SUPPORTED | PARTIAL | PARTIAL | 原文 `is a possibility to find` 被写成"方法是"。我按"方法陈述成立"放过，两者按规则 1 判情态升级 |
| 06 | SUPPORTED | PARTIAL | PARTIAL | 原文 `we use` / `can be seen as`，论断写"agents 组织协作…是自主子系统"。两者按规则 1/2 判升级 |

这不是随机噪声：两个互相不可见的判断在同一处同向偏移，说明问题出在**口径**（我的基准偏松），不是判断力。两者都偏严，方向对使用者是安全的——误伤不会放行坏条目。

**自足轴的分歧是定义歧义**：B 把 `Using this formula...`（12）、`After these steps...`（10）、`For the actual...we use...`（06）判 `DEPENDENT`，理由是句首有指代性状语；A 判 `SELF`，理由是主谓齐全。规则原文只写"指代落在引号外"，两种读法都成立 → 定义必须收紧（见第三节）。

## 二、第 2 轮：变异灵敏度（8 条，5 变异 + 3 对照）

| id | 类型 | 期望 | 实判 | 结果 |
|---|---|---|---|---|
| R1 | 方向反转（quite limited → 充足/规模化） | UNSUPPORTED | UNSUPPORTED | ✓ 精确 |
| R2 | 对照（标定集 08） | SUPPORTED/DEPENDENT | SUPPORTED/DEPENDENT | ✓ 稳定 |
| R3 | 范围放大（we use → 普遍采用） | UNSUP（容 PARTIAL） | PARTIAL | ✓ 检出 |
| R4 | 对照（标定集 04） | SUPPORTED/SELF | SUPPORTED/SELF | ✓ 稳定 |
| R5 | 无中生有的排他（唯一决定） | UNSUPPORTED | PARTIAL | ⚠ 检出但偏轻 |
| R6 | 对照（标定集 03，已知 PARTIAL） | PARTIAL/SELF | PARTIAL/**DEPENDENT** | ✓ 支撑码稳定；自足再次偏严 |
| R7 | 对象替换（Semantic Fingerprint → BIM 标准） | UNSUPPORTED | PARTIAL | ⚠ 检出但偏轻 |
| R8 | 缺席无据（全部实验均未出现失败） | UNSUP（容 PARTIAL） | UNSUPPORTED | ✓ 精确 |

- **检出率 5/5（100%）**：没有一条变异被放行为 SUPPORTED。这是本层最关键的性质。
- **严重度精确率 3/5**：R5、R7 该判 UNSUPPORTED 的判成了 PARTIAL。R7 尤其说明问题——它正是规则 3 写的"对象不是同一个东西"，规则文本明确要求 UNSUPPORTED，审计员仍给了 PARTIAL。
- 对照 3/3 与第 1 轮一致（R6 的支撑码 = 标定集 03 的 PARTIAL），说明混合集里没有整体松口。

## 三、这轮标定得出的三条口径修订

1. **自足轴只管主语**：只有"主语缺失"或"代词作主语"（it/this/these + 谓语）才判 `DEPENDENT`。句首指代性状语（`According to this approach`、`Using this formula`、`After these steps`、`In the presented example`）不算——主谓齐全，单看能读。据此 B 的 3 条与 R6 应改判 `SELF`。
2. **PARTIAL 与 UNSUPPORTED 的边界**：论断的核心**对象或谓语**被替换、或加了排他性最高级（唯一/所有/必然）→ `UNSUPPORTED`，不是 `PARTIAL`。只加强限定词、只放大范围 → `PARTIAL`。据此 R5、R7 应判 `UNSUPPORTED`。
3. **使用方式只能是单侧自动**：`SUPPORTED` 可自动通过（标定中两次误伤都在安全侧）；任何非 `SUPPORTED` 必须人看，判定码只用来分诊，不做自动拦截依据。

## 四、这轮标定的局限

1. **一个模型**：A、B、C 都是同一模型（本会话的 subagent），一致性高不代表多模型一致。换模型要重标。
2. **n 太小**：13 + 8 条，且全部来自 3 篇文献、同一批抽取方的产出。22 篇全量时论断的失败形态可能不在这次覆盖范围内。
3. **基准是单标的**：只有我一人标，没有第二人独立标，所以 11/13 的含义是"与一个口径吻合"，不是"与真理吻合"。
4. **闭卷**：不带上下文，抓不到断章取义。这一层的盲区原样保留。
