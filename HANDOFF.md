# 交接给 OpenCode：后续任务清单

> **状态：已完成（2026-11-09）。T0–T5 全部执行完毕，不要重跑。**
> 结果见 `reports/native-run-01.md`，第三方核验见 `reports/native-run-01-verification.md`。
> **当前有效的任务清单是 `HANDOFF-02.md`（第二轮：C4 补齐）。**

> 面向对象：在 `F:\project\PyProject\Litreview` 打开的 OpenCode，默认 agent = `orchestrator`。
> 生成时间：2026-11-09。上游状态见 `litrev/_probe/RESULT.md`（技术层 9/9 + 4/4 PASS）与 `litrev/_probe/AUDIT_RESULT.md`（论断层审计 5/5 检出）。

## 〇、可以开始了吗

**可以。** 三个前置条件已就位：

| 项 | 状态 |
|---|---|
| 四个角色 | `.opencode/agents/` 下 `orchestrator`(primary) / `extractor` / `checker` / `auditor`(subagent)，frontmatter 仅 `description` + `mode` |
| 默认 agent | `opencode.json` 已设 `default_agent=orchestrator`、`subagent_depth=1`、禁 webfetch/websearch |
| 语料与索引 | 26 个 PDF = 23 篇唯一（3 个完全重复），`WangHoward1991` 无文字层 → **可校验 22 篇**；`_index/manifest.csv` 与该语料一致，**不要重跑 `index`** |

开工时确认两件事：

1. 打开的是 `Litreview` 目录，不是 `Litreview/litrev`（角色文件里的路径都按 `litrev/...` 写的）。
2. 界面左下/顶部的 agent 显示为 `orchestrator`；不是的话按 Tab 切换。若切不到，说明 `.opencode/agents/` 没被识别，停下来把现象贴回来，不要自己改文件名试。

**一个未验证的前提**：OpenCode 的 `read` 工具能否直接读 PDF 没有实测过（上一轮的 PDF 直读是在 WorkBuddy 里做的）。所以 T0 必须先探，不要假设。

## 一、三条纪律（违反任一条，后面的结果都不能用）

1. **不改 `litrev.py`**：它是裁判。发现 bug 写进报告，不要动手。
2. **不覆盖 `litrev/_probe/notes/`**：那是上一轮的基线，本批次全部写到 `_probe/run1/` 与 `_probe/full/`。
3. **不采信自我声明**：只有 `verify` 的退出码、判定码、`auditor` 的判定表算证据。子 agent 说"已完成"不算。

## 二、任务清单

按序执行，**T0–T3 全部通过之前不要开 T4**。每完成一项，报告里必须带命令原文与输出摘要。

### T0 能力探测 + 单篇冒烟（1 个 agent）

- 派 1 个 `extractor`，目标 `参考文献原文/Zhang2006_BP_CaseRetrieval_HighriseStructureForm.pdf`（5 页，最短；注意 PDF 在项目根，不在 `litrev/` 下，与 `litrev.py` 的 `PDF_DIR = BASE.parent / "参考文献原文"` 一致）。
- 只要 3 条引文，输出到 `litrev/_probe/run1/Zhang2006_BP_CaseRetrieval_HighriseStructureForm.md`。
- 目的有两个：验证 `task` 派发链路通；验证 extractor 有没有办法读出 PDF 文本。
- **验收**：① 文件生成且只生成这一个；② 3 条引文带 PDF 物理页；③ 主控运行 `python litrev.py verify _probe/run1/Zhang2006_....md` 退出码 0。
- **失败处理**：若 extractor 报"读不了 PDF/看不到内容"，说明 OpenCode 侧没有 PDF 文本通道。此时停下来，把失败原文贴回来，**改用主控预导出 txt**（与 `_probe/texts/` 同一格式），不要自己发明第三条路。

### T1 并行 3 篇，对照基线（同一条消息内 3 个 task）

- 目标：`Napps2021_BIM_VariantRetrieval_CBR`、`Ayzenshtadt2016_ThinkingWithContainers_ICAART`、`MaherGomez1997_CBR_in_Design`。
- 输入与契约与上一轮**完全相同**（每篇 3 条命题，第 3 条选偏门），唯一差别是 OpenCode 原生 `task` 派发。
- 输出：`litrev/_probe/run1/<文献>.md`。
- **验收**：① 3 个文件齐全、无互相覆盖；② `verify` 9/9 PASS（基线是 9/9，出现 `PARAPHRASE`/`MISSING` 即为回归，要写清差在哪一句）；③ 报告里给出"本轮 3 篇在同一条消息内派发"的证据（各自返回时间或子会话 id）。
- 这一项同时把**原生并行**与**产出质量**一起测了。基线文件在 `_probe/notes/`，同题同契约，可直接逐条比对措辞与页码。

### T2 核验（1 个 checker）

- 派 `checker`，对 `_probe/run1/` 下全部 4 个 md 跑 `verify`，出待改清单。
- **验收**：报告含命令、退出码、各判定码计数、总条数；末尾必须有"本次未验证论断层"的声明。
- 注意副作用：`verify` 会把 `*_引文核验.md` 写在源文件同目录（`litrev.py` 没有 `--out` 参数），`_probe/run1/` 会被这些文件填满，属正常。报告里列出生成了哪些，便于之后清理。

### T3 审计（1 个 auditor）

- 派 `auditor`，把 `_probe/run1/` 里全部条目按 `(id, 论断, 引文, 页码, 出处)` 五元组交给它，判定标准用 `litrev/_probe/AUDIT_CONTRACT.md`（**不要临时改口径**）。
- **验收**：① 输出是规定格式的表格，每行"依据"列是引文原词；② 给出与 `_probe/audit/run_A_B_v1.md` 的一致率（那一轮支撑轴 11/13）。
- **纪律**：非 `SUPPORTED` 的条目不要自行改写稿件，只列清单交给人。

### T4 全量抽取（19 篇，5 批）

前置：先写 `litrev/_probe/CONTRACT_P1.md`——把抽取字段从"3 条命题"升级为 `参考文献原文/文献综述_结构化提问清单.md` 里 P1 的 7 个字段（一句话主张 / 问题域 / 表示形式 / 相似性或检索机制 / 系统形态 / 评价方式 / 明确写出的局限），每个字段后面必须跟一条逐字引文 + PDF 物理页；字段缺失写"未涉及"，找不到引文写 `NOT_FOUND` 并列出查过的页。**先写契约再派活**，不许边跑边改。

分批（按页数均衡，每批 = 一条消息内并列 N 个 `task`）：

| 批 | 文献（页数） | 合计 |
|---|---|---|
| B1 | Zhang2006(5)、Ahmed2013(10)、Soibelman2000(10)、vanEngelenburg2023(10)、delasHeras2014(12) | 47p |
| B2 | Borner1993(11)、MaherGomez1996(11)、Sabri2017(11)、Roith2017(17)、Xia2025(17) | 67p |
| B3 | Rodrigues2017(18)、Gu2024(20)、Maher1987(21)、AamodtPlaza1994(21)、Liao1998(23) | 103p |
| B4 | Sriram1985(22)、Zhao2023(22)、Survey2025(27) | 71p |
| B5 | SharmaThesis(151) 单独一批 | 151p |

- 输出 `litrev/_probe/full/<文献>.md`，一篇一个文件，不许合并。
- **已知陷阱（不要写进派发内容，等于替 agent 算好了）**：B2–B4 里有 4 篇的期刊印张页码与 PDF 物理页不一致（Sriram1985、Rodrigues2017、MaherGomez1996、Sabri2017）。这几篇是核验重点，看它报的是不是物理页。
- B5 是 151 页学位论文：要求它**只抽指定范围**（摘要 + 与平面检索相关的 2–3 节），并在笔记里写明抽了哪几节，不要全文扫。
- **每批完成后立刻跑 `verify`**，不要攒到最后——一批错了只返工那一批。

### T5 汇总（1 份报告）

写 `reports/native-run-01.md`：批次与篇数、`verify` 判定码统计（PASS / PAGE / PARAPHRASE / MISSING / NOPAGE / ZHQUOTE 各几条）、`auditor` 判定统计（SUPPORTED / PARTIAL / UNSUPPORTED）、失败清单（现文 / 原文 / 位置）、与上一轮基线的差异、遗留问题。

### T6 暂缓：矩阵校验

`文献对比与系统特征表2.xlsx` 与稿件目录在当前仓库里都不存在，`matrix` 没有对象。等综述底稿建表后再跑，不在本轮范围。

## 三、派发模板（orchestrator 直接复用）

```
task(extractor):
  读：参考文献原文/<文献>.pdf（只读这一篇；PDF 在项目根，不在 litrev/ 下）
  写：litrev/_probe/full/<文献>.md（只写这一个文件）
  契约：litrev/_probe/CONTRACT_P1.md
  字段：7 个字段，每字段一条逐字引文 + PDF 物理页
  禁止：运行 python / 读 litrev.py / 读 _index/ / 改别人的文件
  找不到：写 NOT_FOUND 并列出查过的页，不许编。
```

## 四、跑完之后怎么回填

把这三样带回来，我这边做机械取证（用 `Opencode_Subagent/tools/opencode_forensics.py --db`，只读快照，不动你的库）：

1. `reports/native-run-01.md`
2. `litrev/_probe/run1/` 与 `litrev/_probe/full/` 的目录清单
3. 若要看并行是否真并行，只需给出本次会话的 session id（取证脚本会自己去 `~/.local/share/opencode/opencode.db` 里算 `part` 时间区间重叠）

## 五、已知风险（提前说，别到时候当故障排查）

1. **无 git 仓库**：OpenCode 的项目根按当前目录算，`.opencode/agents/` 能正常识别；但不要指望 `git diff` 之类的回溯。
2. **无 permission 块**：四个角色都有完整工具权限，"只写自己那一个文件"目前只靠正文约束。要硬隔离得加 `permission` 块（`read` 排除 `litrev.py` 与 `_index/` 是最值钱的一条），但那需要重启 OpenCode，建议放到本轮跑通之后再做。
3. **`verify` 会写同目录报告**：`_probe/full/` 里会混进 `*_引文核验.md`，属预期。
4. **`SharmaThesis` 151 页**：最容易在中途丢上下文的一篇，出错优先怀疑它。
5. **`WangHoward1991`（130 页纯扫描）不在 19 篇里**：要引它得先 OCR，本轮不处理。
