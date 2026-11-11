# HANDOFF-18：`D-04` 选 α 落地（换引文 1 条）+ 冷启动测试待输入

> 本轮两件事：① `D-04` 按 α 落备料，待你重启后派 1 条定点重判；② **冷启动测试在当前语料库做不了**，
> 需要你提供 2–3 篇未入库的 PDF（理由见 §五，这是唯一还差「从没做过」的那一步）。

## 一、这次派什么

| 项 | 值 |
|---|---|
| agent | `auditor-fix-b6`（本轮新生成，51 个 agent） |
| 输入 | `litrev/_probe/audit/FIX_B6.md`（戳 `1310e0ea75`，1 条 `B2-08`） |
| 输出 | `litrev/_probe/audit/out_FIX_6.md`（**必须带下划线**，`out_FIX6.md` 会被 `audit-count` 命中） |
| 性质 | 闭卷、定点重判；**论断一字未动，只换了引文**（p.6 → p.10） |

已完成的改动（不要重做）：

1. 卡片 `full/MaherGomez1996_CBR_StructuralDesign.md` §3 引文换成同篇 p.10 的直接句，页码改 `p.10`。`verify` 单卡 **7/7 PASS**。
2. `batch --only B2` → 变动 **1 条**，`FRAG_B2` 戳 `05632596fd → 1310e0ea75`（与 round-31 的预演值**逐字相同**）。
3. `BATCHES.json` 注册 `fix_b6`，生成器产出 `auditor-fix-b6.md`，`gen --check` **51/51 同步**。

## 二、派发前放行条件（`check.py` 预期红 6 项，**这是备料态，不是坏了**）

```
✗ audit-stale        B2 全 16 条「输入戳变、判定还是旧戳」
✗ audit_prep sample / golden / cases / sample S2 / cases C2
                     同因：load() 发现 B2-01…B2-16 的输入戳与 out_B2.md 判定戳不一致
```

**为什么红**：判定戳是**文件级**的，改一条引文就让 `FRAG_B2` 整批换戳，16 条全部「过期」。
**怎么办**：`reseal` 重封 `out_B2.md` 后 6 项全绿。**不要手工改戳、不要重跑 `batch`、不要重建参考集。**

其余 8 项应绿（`verify` 138/138、`card-check` 20/20、`audit-count` `S138/P0/U0`、`gen` 51/51）。

## 三、派发词（逐字粘贴）

```
按 HANDOFF-18.md 做定点重判，用 auditor-fix-b6 这个子代理。
```

回来回一行：`已写入 out_FIX_6.md：1 行`，加 task id。

## 四、回来后验收（主控做）

1. `out_FIX_6.md` 首行 `> 快照 sha1: 1310e0ea75`；表头逐字照抄输入；1 行 `B2-08`；合计行齐全。
2. 依据列必须**在新引文内**逐字连续命中（≤15 字）。`reseal` 门槛③会查，主控先自查一遍。
3. `python litrev/litrev.py reseal --fix-input FIX_B6.md --fix-out out_FIX_6.md`。
   三门槛：定点戳同源 / 变更集 `{B2-08}` 全覆盖 / 依据命中。全过才重封 + 重算合计 + 追加 `RESEAL.md`。
4. 跑 `python tools/check.py`，预期 **13/13 绿**、`audit-count` 仍 `S138/P0/U0`（若新判 `PARTIAL` 则变 `S137/P1/U0`，如实记）。

### 验收时的两个已知副作用（必须记，别当故障）

- **`SAMPLE_S2.md` 的 `--check` 会持续红**：`build_sample()` 用**当前批次内容**重建文本再与冻结件逐字比，
  而 `S04` 的引文正是这次改的那条。这不是戳的问题，`reseal` 治不了。
  ⇒ **`out_S2.md` 的 11/12 里，`S04` 那条自此失效**（它判的是旧引文），有效样本降为 11 条。
  报告已按此记：S2 与 α 互斥，只能保一个。
- `CASES_SELF_C2` / `GOLDEN` / `CASES_SELF` 若 `--check` 仍红，先确认它们是否含 `B2-08`；
  含则同上，不含则是别的原因，按 `audit-stale` 查。

## 五、冷启动测试：现在做不了（硬约束）

想找一个「从未进过卡片与判定表」的文献做冷启动，实测**一个都没有**：

| 类 | 篇数 | 为什么不能用 |
|---|---|---|
| 已有 `full/` 7 节卡片 | 20 | 已判过、已在 138 条里 |
| 已有 `notes/` **条目式**卡片（`MaherGomez1997`、`Napps2021`） | 2 | 不是 7 节，`batch` 抓不到；改成 7 节等于重写，且规则明令 notes/ 原地不动 |
| 文件名不规范、内容与已入库重复 | 3 | `manifest.csv` 标了 `duplicate_of` |
| 文字层不可用（`WangHoward1991`，0.0 词/行） | 1 | 需 OCR |

⇒ **要跑冷启动，得你提供 2–3 篇不在 `参考文献原文/` 里的 PDF。** 放置方式：

```
参考文献原文/<Author><Year>_<短名>.pdf     # 文件名主干必须含 AuthorYYYY，否则抽取工算不出引用标注会拒派
```

然后在 `litrev/aliases.json` 里加一条（值是该文献第一作者姓氏的写法，如 `["Smith"]`），跑：

```bash
python litrev/litrev.py text --only <stem>     # PDF → texts/<stem>.txt，看词/行是否 ≥3
python tools/gen_subagents.py                   # 自动生成 ex-<slug>（无卡片才会生成）
python tools/gen_subagents.py --check
```

### 冷启动要测的三个数（这是「能不能生产」的唯一证据）

| # | 测什么 | 怎么算 | 现在有数吗 |
|---|---|---|---|
| 1 | **抽取产能**：从 txt 到 7 节卡片要几轮、红几项 | 派 `ex-<slug>` → `card-check` / `verify` / `card-coverage` | 只有 n=1（`Ayzenshtadt2016`，一次过） |
| 2 | **判定产能**：7 节进判定表要几轮、几条落边界 | 建批次 → `auditor-*` → 边界条数 / 7 | 只有 n=1（同上，边界 1/7 ≈ 14%） |
| 3 | **边界成本**：每条边界要几轮人工裁决 | `DISPUTED.md` 新增条目数 × 每条的轮次 | 3 天里 4 条（`D-01…D-04`），平均 ~1.5 轮/条 |

现在的产能证据是 **n=1**。任何「生产就绪」的说法都越过了这个样本量能支撑的范围。

## 六、本轮明确不做

- **不填 C2**（决定停 ③）：阳性分母停在 11/13，`CASES_SELF_C2.md` 保持空白、`_v1_claimlevel.md` 存档不动。
  `RUNBOOK §七 第 15 条` 已记 A/C 决议，C2 的「有效读数」一栏记「已执行、读数无效」。
- **不拍 ④ 漂移标尺**：它的价值依赖稳定新样本流入，等冷启动有数据再定。
- **不改 `AUDIT_CONTRACT.md`**。
