# round-41：`REST_B11`（P3，地下车库/地下空间 6 篇）闭卷审计 —— 23 条判定与裁决

> 日期：2026-11-12 ｜ 批次 `rest_b11` ｜ 输入 `REST_B11.md`（快照 `6d5c7ea415`）｜ 输出 `out_R11.md`
> 派发对象：`auditor-rest-b11`（`AGENT_MAP.md` 已登记，权限仅 `AUDIT_CONTRACT.md` + `REST_B11.md` → `out_R11.md`）
> 结论：**支撑轴 23/23 `SUPPORTED`，`PARTIAL` 0 / `UNSUPPORTED` 0；自足轴 `SELF` 22 / `DEPENDENT` 1（`R11-12`）。工具口径已入册：`R11 23 23 0 0 22 1 ✓`，全表 237 条自洽。** 本批入册，`R11-12` 与 `R11-14` 记为已知问题（附修法），本轮不触发返工。

## 一、审计前的门禁（先证输入不是过期稿）

`checker` 在派发前跑 `audit-stale --check`（原始输出）：

```
批次输入 237 条 · 卡片 38 篇 / 266 节 / 237 条引文
判定依据与卡片一致：237/237
```

`REST_B11.md` 的 `> 快照 sha1: 6d5c7ea415` 与六篇卡片当前内容一致，0 条过期、0 条对不上卡片；当时唯一告警是 `R11：23 条待重审 · 没有判定输出`，即「输入就绪、判定缺位」，正是本次要补的那一格。派发词据此写明：**第一行原样抄 `> 快照 sha1: 6d5c7ea415`**。

## 二、判定结果（文件为准，不以 `task_result` 为准）

`litrev/_probe/audit/out_R11.md` 结构核对：

| 项 | 实测 | 要求 | 结论 |
|---|---|---|---|
| 第一行 | `> 快照 sha1: 6d5c7ea415` | 与输入逐字一致 | ✓ |
| 表头 | 5 列，与输入 §表头逐字同 | 照输入表头 | ✓ |
| 数据行 | 23 行（L5–L27，`R11-01`…`R11-23`） | 23 条、行序同输入 | ✓ |
| 合计行 | `合计：23 条（SUPPORTED 23 / PARTIAL 0 / UNSUPPORTED 0；DEPENDENT 1）` | 末行一合计 | ✓ |
| 表外文字 | 无 | 只写表格 + 合计 | ✓ |

分布与逐条（`依据` 列为审计员给出的引文原词片段）：

| id | 支撑 | 自足 | 依据 | 文献·节 |
|---|---|---|---|---|
| R11-01 | SUPPORTED | SELF | `more than 15%` | LinRonghui·§1 |
| R11-02 | SUPPORTED | SELF | `paper studied` | LinRonghui·§2 |
| R11-03 | SUPPORTED | SELF | `Table 1` | LinRonghui·§3 |
| R11-04 | SUPPORTED | SELF | `paper compares` | LinRonghui·§5 |
| R11-05 | SUPPORTED | SELF | `are obvious` | LinRonghui·§6 |
| R11-06 | SUPPORTED | SELF | `no advantage` | LinRonghui·§7 |
| R11-07 | SUPPORTED | SELF | `in both cases` | Olga·§1 |
| R11-08 | SUPPORTED | SELF | `solid supports` | Olga·§2 |
| R11-09 | SUPPORTED | SELF | `2D models` | Olga·§3 |
| R11-10 | SUPPORTED | SELF | `Plaxis 2D` | Olga·§5 |
| R11-11 | SUPPORTED | SELF | `conforms` | Olga·§6 |
| **R11-12** | SUPPORTED | **DEPENDENT** | `只有通过合理的优化措施` | matao·§1 |
| R11-13 | SUPPORTED | SELF | `车位利用率低` | matao·§2 |
| R11-14 | SUPPORTED | SELF | `分析其优化措施并加以探讨` | matao·§5 |
| R11-15 | SUPPORTED | SELF | `建筑设计工作者必须充分考虑` | yechunhai·§1 |
| R11-16 | SUPPORTED | SELF | `还是在地下汽车库` | yechunhai·§2 |
| R11-17 | SUPPORTED | SELF | `36~38平米/辆` | yechunhai·§3 |
| R11-18 | SUPPORTED | SELF | `科学应对设计问题可有效提升` | zhengmei·§1 |
| R11-19 | SUPPORTED | SELF | `四大常见问题及成因` | zhengmei·§2 |
| R11-20 | SUPPORTED | SELF | `提出针对性处理策略` | zhengmei·§5 |
| R11-21 | SUPPORTED | SELF | `涉及平面布置、柱网车位` | zhouyulong·§1 |
| R11-22 | SUPPORTED | SELF | `8m×8m或8m×9m` | zhouyulong·§2 |
| R11-23 | SUPPORTED | SELF | `提供新思路` | zhouyulong·§5 |

## 三、工具口径（`checker` 复跑，非自我声明）

```
R11        23    23     0     0    22     1  ✓
合计        237   231     6     0   203    34
口径：237 条 · SUPPORTED 231 / PARTIAL 6 / UNSUPPORTED 0 · SELF 203 / DEPENDENT 34
非 SUPPORTED：6/237 = 2.5%
```

- `audit-stale --check` 复跑已变为 `判定依据与卡片一致：237/237` + `✓ 全部判定的依据与卡片当前内容一致`，R11 不再待重审；
- `audit-count --check` 与不带 `--check` 逐字一致，无差异行；
- 横向相加：14 个批次条数 = 237、SUPP = 231、PART = 6（R10 1 + R9 5）、UNSU 0、SELF 203 / DEP 34，逐列闭合；R11 行 23 = 23+0+0，22+1 = 23。

判定层 214 → 237 的口径推进成立：round-40 新增的 6 篇、23 条引文自此**有判定依据**，不再是「核验绿、支撑轴空缺」。

## 四、我的抽检（4/23 ≈ 17%，超出 10–15% 规程下限）

按固定顺序抽 §1 首条 + 三篇中文的对照项，逐句拿论断与引文对成分（主体/动作/对象/范围/限定强度）：

| id | 论断成分 vs 引文 | 我的判断 |
|---|---|---|
| R11-01 | 「综合成本比主次梁结构低 15% 以上」↔ `comprehensive cost ... more than 15% lower than ... main and secondary beam floor structure`；主体、对象、数值、方向全对 | 判 SUPPORTED 正确 |
| R11-02 | 「评估三种结构体系之间作选择时的经济效益」↔ `studied economic efficiency of selecting ... structure system ... for the roof of underground garage` | 判 SUPPORTED 正确 |
| R11-12 | 论断以「认为」开头而无主体；引文 `只有通过合理的优化措施…才能…` 本身也是无主泛论句（`实现`的主体不在引文内） | 判 DEPENDENT 正确 |
| **R11-14** | 论断「本文**从**…角度，**对**优化措施**进行分析**与探讨」↔ 引文「本文**将**从…角度，**分析其**优化措施**并加以**探讨」：**「将」被删**，将来时→一般现在时 | **偏松**：按 `AUDIT_CONTRACT.md` §三.1「情态/强度」与 §五.2「只削弱语气强度/范围 → `PARTIAL`」，应判 `PARTIAL`，判 `SUPPORTED` 松了一档 |
| R11-17（观察项，未计入误判） | 论断「规模数据以**单车的面积指标**来表示，即依照36~38平米/辆…」↔ 引文「依照36~38平米/辆的**单车位规模要求**」；「面积指标」是对「平米/辆…规模要求」的概括，非引文原词 | 可判 SUPPORTED，但属术语概括，若下轮抽检严格口径会翻成 PARTIAL |

**基线比对（防止把 100% 当成偏松证据）**：本批 0/23 非 SUPPORTED，历史 6/214 = 2.8%。在 p=0.028 下 P(X=0|n=23) ≈ 0.97²³ ≈ **0.52**——「23 条全 SUPPORTED」与既有基线**并不冲突**，本身不构成系统性偏松的证据；真正的偏松信号是上面这条**具体的** `R11-14`。

## 五、裁决

1. **`out_R11.md` 入册**（工具口径自洽、快照符、行序符、表外无杂文），237 条口径生效。不在主控侧改 `out_R11.md` 任何一格。
2. **`R11-12`（matao §1，`DEPENDENT`）记为已知问题**，本轮不返工。理由：支撑轴 `SUPPORTED`，缺陷仅自足轴「无主语」，不影响「是否撑得起」；且按规程返工需 qx 改 `matao` 卡片 §1 论断 → `batch` 报变动 → **整批 23 条重审**，为 1 行代价过大。修法留档（下轮若动 `matao` 一并改）：论断补归属主语，照 LinRonghui §7（`作者指出…`，R11-06 判 `SELF`）的既有写法：`作者认为，只有通过合理的优化措施和细心的设计…`。
3. **`R11-14`（matao §5，判 `SUPPORTED` 但我判偏松）记为已知问题**，不就地改判、不整批重做。理由：① 单条偏松，与基线并不构成「整批系统性偏松」（§四 的二项测算）；② 规程要求「抽检出现误判 → 整批重审」，但本次抽检是我的人工裁决而非工具固定种子抽检，样本 4 条、仅 1 条落在边界，重启 23 条重审等于重掷一次骰子。修法留档：把 §5 论断改成与引文同态——`本文将从地下车库建筑设计的角度，分析其优化措施并加以探讨。`，或换一条 p.2–p.3 描述已完成工作的引文。
4. **`R11-17` 列为下轮固定抽检项**（术语概括类，`AUDIT_CONTRACT.md` §三.3 的边界）。
5. **不派 `qx-` 返工**：本轮两条已知问题都不是「引文查不到」或「论断被证伪」，且 `qx` 的授权是改引文范围/扩句，改论断主语与时态不在其授权范式的中心；跳过本轮返工可避免为 2 行文字触发一次全批重审，同时把改动理由、改法、影响面（整批重审）全部留档。

## 六、仍未覆盖的部分（下轮验证项）

- **固定种子工具抽检尚未做**：规程要求 `litrev.py sample --rate 0.12 --seed 42`，但 `sample` 从 `full/` 候选池取样并新建批次，需先登记批次 + `gen_subagents.py` 生成 `auditor-sample-s3`；本轮以主控人工抽检 4/23 代替，口径上属「人工裁决」而非「工具抽检」，不计入抽检统计。
- **节位错配不属审计范围**：`AUDIT_CONTRACT.md` 明确「不判引文内容是否完整回答了节名」。本批 `R11-22`（柱网尺寸写进「问题域」）、`R11-19`（摘要式综述写进「问题域」）这类**节位可疑**项，`verify`/`audit-*` 全查不出，只能人读卡片（round-40 §四 已记为待盯项），本批维持原判。

## 七、产物

- 判定表：`litrev/_probe/audit/out_R11.md`（23 行 + 合计，首行快照 `6d5c7ea415`）
- 批次输入：`litrev/_probe/audit/REST_B11.md`（23 条；19 个「未涉及」节不入表）
- 卡片：`litrev/_probe/full/` 六篇（round-40 落盘，`verify` 23/23 PASS）
- 本报告：`reports/round-41-rest-b11.md`
