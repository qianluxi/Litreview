# 交接给 OpenCode：第二轮（C4 补齐）

> 面向：在 `F:\project\PyProject\Litreview` 打开的 OpenCode，默认 agent = `orchestrator`。
> 生成时间：2026-11-09。上游：`reports/native-run-01-verification.md`（第三方核验，非本轮执行者所写）。

## 〇、开工前只读这三份

1. `reports/native-run-01-verification.md` —— 上一轮的核验结论，本文件的所有数字都出自这里
2. `litrev/_probe/AUDIT_CONTRACT.md` —— C4 判定标准，**含第五节口径修订，那是唯一有效版本**
3. 本文件

**`HANDOFF.md` 是上一轮的清单，T0–T5 已全部完成，不要重跑。** 它的 PDF 路径缺陷也已修过。

---

## 一、上一轮结论：可以当基线，不需要重验

| 项 | 数字 | 核验方式 |
|---|---|---|
| 引文层 | **143/143 PASS**，退出码全 0 | 重跑 `verify` + 绕开 `litrev.py` 用 PyMuPDF 逐页复核，两条独立路径一致 |
| 印张偏移陷阱 | 4 篇（−3 / +47 / +41 / +49）**全部报物理页** | 逐页子串匹配，无一条落在印张页 |
| 派发 | 26 次 `task` : 26 个子会话，**1:1 无孤儿** | `opencode.db` 只读解析 |
| 并行 | 5 组，加速 1.90 / 4.44 / 2.22 / 3.06 / 2.52x，整体 **1.9x** | `part.state.time` 区间重叠 |
| 耗时 | 墙钟 27.6 分钟，26 次 task 累计 53.5 分钟 | 同上 |
| 成本 | **$0.4638**，extractor 占 80%，验证+审计合计 <2% | `step-finish` 的 tokens 与 cost |
| 越界 | 23 个 extractor 各写 1 个文件，0 个读过 2 篇 txt | 工具调用逐条审计 |

### 三处必须记住的纠正

**1. PDF 直读：工具层面不报错，这才是危险的地方。**
上一轮报告写「`read` 返回 ERROR」，实际库里的记录是：

```
tool     = read
status   = completed
output   = "PDF read successfully"
metadata = {"loaded": []}        ← 0 页被加载
```

那句 `Cannot read pdf (this model does not support pdf input)` 只出现在模型侧的附件里。**任何只看 `status == completed` 就继续的编排，会拿着空内容往下编，而且不会收到任何错误。** 所以本轮继续走「主控预导出 txt」，不要重试 PDF 直读。

**2. 131 条里有 48 条是句中片段，这是本轮的主要工作量。**
形式判据（首字母小写 / 未以句末标点结尾）命中 48 条 = 36.6%，分布在 12 篇，最集中的是 Borner1993、MaherGomez1996、Zhang2006 各 7 条。这些 `verify` 全过，但自足轴大概率判 `DEPENDENT`。

**3. 分批按篇数均分是错的。**
B2 批 5 个任务里 4 个在 226 秒内结束，Borner1993 跑了 441.9 秒，整批被它拖住，加速比只有 2.22x（比不并行的 4.44x 差一半）。下一轮排班看预估耗时，不看篇数。

---

## 二、本轮任务（按顺序，不要跳）

### T1 · 48 条片段审计（P0，同一条消息内 3 个 task）

批次文件已备好，**不需要你自己拆**：

| 批次 | 文件 | 条数 |
|---|---|---:|
| B1 | `litrev/_probe/audit/FRAG_B1.md` | 16 |
| B2 | `litrev/_probe/audit/FRAG_B2.md` | 16 |
| B3 | `litrev/_probe/audit/FRAG_B3.md` | 16 |

分批方式是**按文献轮转**，同一篇的条目被故意打散到不同批次，避免一个审计员看到同篇 7 条后猜出上下文、把 `DEPENDENT` 判成 `SELF`。

- **派 3 个 `auditor`，同一条消息内并列**，每人只读自己那一份文件。
- **闭卷纪律**：不许读 PDF、不许读 `full/*.md`、不许读别人的批次文件。只依据文件里给出的论断与引文判定。
- **验收**：① 三份表齐全，行序与批次文件一致，条目数 = 16/16/16；② 每条「依据」列能在该条引文里逐字找到（你在汇总时抽查，至少 15 条）；③ 合计行数字与逐行统计一致。

### T2 · 落成待改清单（P0）

把 T1 的三份判定合成 `litrev/_probe/audit/C4_FRAG_RESULT.md`：

1. 总判定分布（SUPPORTED / PARTIAL / UNSUPPORTED；SELF / DEPENDENT）
2. 按文献分布表
3. **待改清单**，每条四件套：`现文论断` / `引文原文` / `缺什么` / `位置`（文献 + 字段 + 页码 + 源文件行号）
4. 与 v1 标定的对照：上一轮 12 条是 7 SUPPORTED / 5 PARTIAL / 0 UNSUPPORTED，`_probe/audit/run_C_v1.md` 的变异检出是 5/5

- **纪律**：`PARTIAL` 与 `UNSUPPORTED` 一律只列不改，交给人。只有 `SUPPORTED + DEPENDENT` 这一类允许进入 T3 自动处理（引文内容没问题，只是句子被截断）。

### T3 · 片段扩句（P1，派 extractor）

对象：T1 里判为 `SUPPORTED + DEPENDENT` 的条目。

- 每条派一个 `extractor`（可多条并列），要求它**只读该篇 PDF**，找到这句原文的完整句子边界，把引文向前/向后扩到完整句。
- **只许扩大边界，不许改写、不许拼接不相邻文本、不许换句子**。扩完必须是 PDF 里连续的一段逐字文本。
- **扩完由你自己重跑 `verify`**，不要交给 extractor 自证。判 `PAGE` 就是失败——多页跨页时按句拆成两条，各自标页。
- 已在上一轮出现过的 OCR 断词（见第五节）保持原样扩，不要顺手改正字，`verify` 的归一化能过；词形还原是成稿阶段的事，另记。

### T4 · 剩余 83 条支撑轴审计（P1，T3 之后）

48 条片段只覆盖**自足轴**的风险。支撑轴（论断是否超出引文）在其余 83 条里同样存在，而且 v1 基线已经证明它存在：12 条里有 5 条 `PARTIAL`，全部是「缺席命题」——论断写了「该文没有给出 / 未报告」，单条引文证明不了。

成本上没有任何理由不做：上一轮 auditor 审 12 条花了 $0.0071，审满 131 条不到 $0.1。

- 做法与 T1 相同：按文献轮转分 5–6 批，每批 14–17 条，同一条消息内并列派发。
- 必须放在 T3 之后，因为扩句会改引文，重审要用改后的版本。
- 批次文件由你自己按 T1 的格式生成，或在 T3 完成后再来找我要。

### T5 · permission 硬隔离（P2，需重启）

上一轮的干净是**行为层**的：23 个 extractor 恰好都只写了一个文件，没有机制拦着。而且 `checker` 读过 1 次 `litrev.py`——它是裁判方，风险低，但这条正好是第一个该堵的口子。

建议规则（`permission` 是 1.18.25 的键，改完**必须重启 OpenCode**）：

```yaml
# extractor.md
permission:
  read:
    "*": allow
    "litrev/litrev.py": deny
    "litrev/_index/*": deny
    "litrev/_probe/full/*": deny
    "litrev/_probe/notes/*": deny
  edit:
    "*": deny
    "litrev/_probe/full/*": allow

# auditor.md —— 保证闭卷
permission:
  read:
    "*": deny
    "litrev/_probe/audit/*": allow
```

三条注意事项：

1. **不要写 `read: {"*": deny}` 以外的全量 deny 给 extractor**。实测机制是：`pattern == "*" && action == "deny"` 时该工具**根本不注册**，模型看不到 `read`，它会转而用别的方式绕，你反而拿不到拒绝证据。
2. 路径按相对 worktree 匹配，写法必须与上面的前缀一致。
3. 改完先跑一条冒烟：确认 extractor 仍能读 txt、仍能写 md，只是读不到 `litrev.py`。**验收方式是让它主动试一次越界并拿到拒绝原文**，不是「看起来没报错」。

### T6 · 本轮不做

| 项 | 原因 |
|---|---|
| 再抽新文献 | 22 篇已抽完，质量缺口在论断层，不在覆盖量 |
| 矩阵校验 | `文献对比与系统特征表2.xlsx` 仍不在仓库，没有对象 |
| `WangHoward1991` | 130 页纯扫描无文字层，要 OCR，不在本轮 |
| 续写综述正文 | 先把 C4 清干净再写，否则写完还要整篇返工 |

---

## 三、派发模板

```
task(auditor):
  读：litrev/_probe/audit/FRAG_B{1|2|3}.md（只读这一份）
  判定标准：litrev/_probe/AUDIT_CONTRACT.md（含第五节口径修订）
  任务：对该文件全部 16 条按两轴独立判定，输出规定表格 + 合计行
  禁止：读 PDF、读 full/*.md、读其他批次文件、查外部资料
  已知：这些引文全部已通过 verify（逐字存在、页码为物理页），你不判真伪与页码
```

```
task(extractor):
  读：参考文献原文/<文献>.pdf（只读这一篇）
  改：litrev/_probe/full/<文献>.md 中第 N 条引文（只改这一条）
  要求：把引文向前/向后扩到完整句子边界，逐字连续，不改写、不拼接、不换句
  禁止：改论断、改页码（跨页则拆成两条各自标页）、改动其他条目
  交付：旧引文 / 新引文 / 新页码 / 扩展了几个词
```

---

## 四、验收口径（怎么算通过）

| 任务 | 通过 | 不通过 |
|---|---|---|
| T1 | 48 条全部有判定；依据列可逐字回溯；合计行自洽 | 有条目被合并、跳过，或依据列写的是「文意相符」这类非原文词 |
| T2 | 待改清单每条都能定位到源文件行号 | 只给统计不给位置 |
| T3 | 每条扩句后 `verify` 退出码 0，且新增文本与旧引文连续 | 出现 `PAGE`、或 extractor 自己说「扩好了」但没有 `verify` 输出 |
| T4 | 同 T1 | — |
| T5 | 越界被拒的**原文**（`The user has specified a rule...`） | 「应该拦住了」 |

---

## 五、已知坑（提前说，别当故障排查）

1. **OCR 断词 9/131 条**，集中在 Borner1993（7 条里 6 条）：`Structural similarit y`、`kno wledge a v ailable`、`whic h`。`verify` 的归一化会去掉空格所以全过，但直接粘进综述没法看。扩句时**原样保留**，成稿阶段统一还原。
2. **跨页扩句会判 `PAGE`**：`verify` 按单页查找，句子跨页必须拆成两条。
3. **`verify` 会在源文件同目录写 `*_引文核验.md`**（没有 `--out` 参数），`_probe/full/` 里的核验报告是上一轮留下的，不要当垃圾清掉。
4. **审计严重度会偏轻**：v1 变异测试里该判 `UNSUPPORTED` 的 2/5 被判成 `PARTIAL`，但 5/5 变异无一被放行为 `SUPPORTED`。所以 **`SUPPORTED` 可自动放行，非 `SUPPORTED` 必须人看**，不要拿它做自动拦截。
5. **不要改 `litrev.py`**。它是裁判，改了之前所有判定作废。发现 bug 写进报告。
6. **不要采信自我声明**。子 agent 说「已完成」不算，只有 `verify` 退出码与判定码算。

---

## 六、跑完带回来什么

1. `litrev/_probe/audit/C4_FRAG_RESULT.md`
2. T1 三份原始判定表（`audit/out_B1.md` 等，由你落盘）
3. 扩句前后的引文对照（旧 / 新 / 页码 / 扩展词数）
4. 本次会话的 session id —— 我做机械取证（`Opencode_Subagent/tools/opencode_forensics.py`，只读快照），核这轮的派发数、并行加速度、有没有越界读写

一句话：**这一轮不是再抽，是把「引文真实」升级成「引文真的能支撑论断」。** 143/143 只证明了前者。
