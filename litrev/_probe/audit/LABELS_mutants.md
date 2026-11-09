# 变异集人工基准（审计员不可见）

"检出"的判定口径：**支撑判为 SUPPORTED 即算漏检**（不论它是否在"缺什么"里补了一句）。因为审计层的职责是给出可机读的判定码，判定码放行而理由里埋一句提醒，等于没拦住。

| id | 类型 | 期望 | 依据 |
|---|---|---|---|
| R1 | 方向反转 + 规模放大 | UNSUPPORTED（可接受 PARTIAL） | 原文 `quite limited`；`sufficient to show the retrieval process` 只针对流程演示，不针对规模化实验 |
| R2 | 原样对照 | SUPPORTED / DEPENDENT | 与标定集 08 同一条，用于测稳定性 |
| R3 | 范围放大（规则 2） | UNSUPPORTED（可接受 PARTIAL） | `we use a container-based structure` → "普遍采用"；`can be seen as` → "都是" |
| R4 | 原样对照 | SUPPORTED / SELF | 与标定集 04 同一条 |
| R5 | 无中生有的最高级（规则 1/3） | UNSUPPORTED | `identifies the features` 不含"唯一/决定相关性" |
| R6 | 原样对照（已知 PARTIAL） | PARTIAL / SELF | 与标定集 03 同一条；若这里判 SUPPORTED，说明审计员在混合集里松了口径 |
| R7 | 对象替换（规则 3） | UNSUPPORTED | 原文是 `Semantic Fingerprint`，不是 BIM 标准 |
| R8 | 缺席无据（规则 4） | UNSUPPORTED（可接受 PARTIAL） | 原文只给"差异为零 → 相似度一"的定义，不含"全部实验"与"未出现失败" |

## 计分方式

- 变异条（5 条）：判非 SUPPORTED 记检出；判 SUPPORTED 记漏检。其中 3 条允许 UNSUPPORTED/PARTIAL 二选一，另 2 条（R5、R7）要求严格 UNSUPPORTED。
- 对照条（3 条）：支撑码必须与标定集一致；R2 的自足码必须为 DEPENDENT。
