# round-40：6 篇新文献首次抽取 + 引文层核验（`LinRonghui2020` / `matao2023` / `Olga2020` / `yechunhai2022` / `zhengmei2025` / `zhouyulong2026`）

> 日期：2026-11-12
> 结论：**6 张卡片全部落盘，7 节结构逐字合规；引文层 23/23 `PASS`（0 `PARAPHRASE` / `MISSING` / `NOPAGE` / `AUTHOR` / `ZHQUOTE`）。论断层（支撑轴）尚未审计——本批未进任何 `REST_B*` 批次，见 §五。**

## 一、派发与输入核对

派发前查 `litrev/_probe/AGENT_MAP.md`，六个 `ex-` agent 均在表内且 `.opencode/agents/` 存在对应文件；六篇 `texts/*.txt` 均存在，六张卡片事先均不存在（`notes=False`），故走「首次抽取」而非返工。

| 文献 | ex- agent | txt | PDF 物理页 | 派发前卡片 |
|---|---|---|---|---|
| `LinRonghui2020_economicanalysisfloor` | `ex-linronghui2020-economicanalysisfloor` | 存在 | 6 | 不存在 |
| `matao2023_undergroundoptimize` | `ex-matao2023-undergroundoptimize` | 存在 | 3 | 不存在 |
| `Olga2020_ArrangementMultistoryUnderground` | `ex-olga2020-arrangementmultistoryunderground` | 存在 | 16 | 不存在 |
| `yechunhai2022_underground` | `ex-yechunhai2022-underground` | 存在 | 3 | 不存在 |
| `zhengmei2025_undergroundparking` | `ex-zhengmei2025-undergroundparking` | 存在 | 3 | 不存在 |
| `zhouyulong2026_undergroundoptimize` | `ex-zhouyulong2026-undergroundoptimize` | 存在 | 3 | 不存在 |

输出路径以 agent 自身的授权为准：`litrev/_probe/full/<文献>.md`（`gen_subagents.py` 的 `FULL_DIR`），**不是** `litrev/_probe/notes/`。`litrev.py` 的 `CARD_DIR` 亦默认为 `_probe/full`（litrev.py:1153），两侧一致。

## 二、验收（文件系统为证据，不以 `task_result` 为准）

六次派发均 `completed`，且 `task_result` 非空；抽查文件内容与回报数字逐一吻合：

| 文献 | 文件字节 | `- 论断：` 行 | `- 引文：` 行 | 未涉及节 | 节标题 1–7 逐字比对 |
|---|---|---|---|---|---|
| `LinRonghui2020_economicanalysisfloor` | 2836 | 7 | 6 | 1（§4） | OK |
| `matao2023_undergroundoptimize` | 1370 | 7 | 3 | 4（§3§4§6§7） | OK |
| `Olga2020_ArrangementMultistoryUnderground` | 2455 | 7 | 5 | 2（§4§7） | OK |
| `yechunhai2022_underground` | 2214 | 7 | 3 | 4（§4§5§6§7） | OK |
| `zhengmei2025_undergroundparking` | 1966 | 7 | 3 | 4（§3§4§6§7） | OK |
| `zhouyulong2026_undergroundoptimize` | 1724 | 7 | 3 | 4（§3§4§6§7） | OK |
| **合计** | — | **42** | **23** | **19** | 6/6 OK |

42 节 = 23 条引文 + 19 节「未涉及」，无缺口。`git status` 显示六张卡片均为新文件（`??`），未出现越权写入（无 `notes/`、无 `_index/`、无其它文献名）。`- 引文：` 每节至多一条，未见同句跨节复用。

## 三、引文层核验（`checker`，6 次并行派发）

六个 `checker` 分别只跑一条 `python litrev/litrev.py verify litrev/_probe/full/<文献>.md`：

| 文献 | 合计 | PASS | 非 PASS | 页码核对 |
|---|---|---|---|---|
| `LinRonghui2020_economicanalysisfloor` | 6 | 6 | 0 | p.4/p.2/p.3/p.3/p.4/p.6 全符 |
| `matao2023_undergroundoptimize` | 3 | 3 | 0 | p.3/p.1/p.1 全符 |
| `Olga2020_ArrangementMultistoryUnderground` | 5 | 5 | 0 | p.1/p.1/p.1/p.8/p.13 全符（另以 `locate` 五句独立复击，相似度均 1.00；`Mohr-Coulomb` 回取为原文的 `Mohr–Coulomb` U+2013，说明定位的是原文） |
| `yechunhai2022_underground` | 3 | 3 | 0 | p.3/p.1/p.2 全符 |
| `zhengmei2025_undergroundparking` | 3 | 3 | 0 | p.1/p.1/p.3 全符 |
| `zhouyulong2026_undergroundoptimize` | 3 | 3 | 0 | p.3/p.1/p.1 全符（§2 那条以「（1）柱网尺寸与停车效率的关系：」开头的引文被判 PASS，非片段裁剪） |
| **合计** | **23** | **23** | **0** | 全符 |

两条需要留档的判定细节：

1. **`yechunhai2022` §3 的「規模」是原文如此，不是卡片笔误。** `checker` 回读 `texts/yechunhai2022_underground.txt` 第 129 行：同一行内「规（划）」为简体 `规`(U+89C4)、「規模」为繁体 `規`(U+898F)，第 130 行又回到简体——OCR/抽取层的繁简混用。**改卡片反而会把 PASS 掉成 PARAPHRASE**，故保留原字。
2. **`Olga2020` 的作者 token 就是 `Olga`**（`file_stem_author` 取年份前字母，litrev.py:312–319），与卡片标注 `(Olga, 2020, p.N)` 相符；不得改成 `Trushko`。

核验同时确认 `audit-stale --check` 输出 `判定依据与卡片一致：214/214`（既有 214 条判定所依据的卡片内容未被本次抽取改动——本批只新增卡片，未改旧卡片）。

## 四、内容层面需要盯的点（不构成 verify 失败，留给审计/人读）

- `matao` / `yechunhai` / `zhengmei` / `zhouyulong` 四篇是 3 页实践型中文短文，`未涉及` 占比高（19/42）。抽查未见「拿相邻问题的技术细节充数」的痕迹：`zhouyulong` 把柱网/车道取值放在 §2 而非 §3，`zhengmei` 未把「研究表明…」的抽象断言填进 §6。但 **§1/§2/§5 的论断是「本文旨在…」式自述**，支撑轴审计时易判 `DEPENDENT`（缺执行者/对象），需 `auditor` 逐条定性。
- `LinRonghui2020` §7 取的是 p.6「从楼面造价看，空心无梁楼盖相比平楼盖并无优势、造价略高」——这是把「该技术在某口径下的劣势」当作作者自述局限，节位归属（§7 vs §1 的反面证据）值得审计时确认。
- `Olga2020` §6 与 §1 共用同一组 20 mm 结论（分别引自 p.13 与 p.1 摘要），页码不同、句子不同，非复用；但摘要句作 §1 主张、结论句作 §6 评价，强度是否一致需审计确认。

## 五、为什么停在核验之后：审计批次缺失（阻塞项，非失败）

阶段顺序要求 `ex-` → `checker` → `auditor-`，并规定「跳过核验直接审计，审计结果作废」。本批核验已绿，但**无法推进审计**，原因有三，均为基础设施缺口：

1. `litrev/_probe/audit/BATCHES.json` 里没有覆盖这六篇的批次（最大到 `rest_b10`，`REST_B10` 只含 Park/Elgaali/Zhu/Qu/Lu 五篇）。
2. `litrev.py batch` **只刷新已存在的** `REST_B#.md` / `FRAG_B#.md`（litrev.py:1596–1601 用 glob 取文件名），**不会新建** `REST_B11.md`；新批次输入需按既有格式（`> 快照 sha1:`、`### R11-01 ｜ 文献 ｜ 节 ｜ p.N`、`- 论断：` / `- 引文：` / `- 源文件：第 N 行`）另行构建。
3. 没有 `auditor-rest-b11` agent（需先登记 `BATCHES.json` 再跑 `tools/gen_subagents.py`）。

故本批 23 条引文的**支撑轴判定为零**，不得在汇总口径里记作「已验证」或「SUPPORTED」。下一步建议（需主控决定是否动 `BATCHES.json` 与重跑生成器）：

```bash
# 1) 在 BATCHES.json 追加 rest_b11（input=REST_B11.md, output=out_R11.md，前缀 R 进 audit-count 口径）
# 2) python tools/gen_subagents.py
# 3) 构建 REST_B11.md（格式照 REST_B10.md，含六篇 42 节的 23 条引文；19 个「未涉及」节不进批次）
# 4) python litrev/litrev.py batch --only B11      # 落快照 sha1
# 5) 派 auditor-rest-b11 → out_R11.md（第一行原样抄输入里的 `> 快照 sha1: ...`）
```

## 六、产物清单

- 卡片：`litrev/_probe/full/{LinRonghui2020_economicanalysisfloor, matao2023_undergroundoptimize, Olga2020_ArrangementMultistoryUnderground, yechunhai2022_underground, zhengmei2025_undergroundparking, zhouyulong2026_undergroundoptimize}.md`
- 裁判派生核验报告（`verify` 自写，非人工）：`litrev/_probe/full/<同上>_引文核验.md` ×6
- 判定表：**无**（本批未审计）
