# 交接给 OpenCode：第四轮（B1–B3 重审）

> 前一轮（`reports/round-03-fix-verification.md`）结论：引文层已全绿，但 **B1–B3 三批共 48 条的判定作废**，需要重审。
> 本文件只列这一件事。做完停下，不要顺手做别的。

## 当前状态（已核实，不要重算）

| 项 | 值 | 命令 |
|---|---|---|
| 引文层 | 19 篇 131 条全部 PASS | `python litrev/litrev.py verify litrev/_probe/full/<文献>.md` |
| 判定表自洽 | 131 条 · S84 / P46 / U1 · SELF112 / D19 | `python litrev/litrev.py audit-count --check` → 退 0 |
| 判定有效性 | **83 条有效（R1–R5），48 条待重审（B1–B3）** | `python litrev/litrev.py audit-stale` |
| 批次输入 | 已刷成卡片当前内容，均带 `> 快照 sha1: ...` | `python litrev/litrev.py batch --check` → 0 变动 |
| 子代理 | 33 个，与角色模板同步 | `python tools/gen_subagents.py --check` |
| 审计契约 | §四 已写明「首行抄戳」、§五.3 与 §七.2 的冲突已消歧义 | `AUDIT_CONTRACT.md` |

`audit-stale --check` 现在退 1，就是那三批。**重审完必须退 0**（已实测退 1，不是打印好看）。

> 契约只改了输出格式与口径适用范围的说明，**两轴判定规则一字未动**，所以 R1–R5 的 83 条判定继续有效，不必跟着重审。

## 任务：重审 B1、B2、B3

三批输入已刷新（`litrev/_probe/audit/FRAG_B1.md` 等，各 16 条）。20 条依据变过的条目（其余 28 条属闭卷整批重跑）：

```
B1-03  B1-04  B1-05  B1-12  B1-13  B1-14
B2-01  B2-03  B2-04  B2-05  B2-08  B2-09  B2-12  B2-13
B3-02  B3-03  B3-04  B3-12  B3-13  B3-16
```

派发规则：

1. 一次一个批次，一个 `task` 一次调用。三批**不要**塞进同一条消息——并发时一旦出现空结果就定位不到是哪条。
2. 派 `auditor-frag-b1` / `auditor-frag-b2` / `auditor-frag-b3`，输入对应 `FRAG_B{n}.md`，输出 `out_B{n}.md`（覆盖旧文件）。
3. 派发提示词里必须写明三条，缺一条就可能白跑：
   - **输出第一行原样抄输入里的 `> 快照 sha1: ...`**（在输入文件第 6 行）。抄错或漏抄 = 来源不明 = 整批作废，`audit-stale` 会报"输出没回写戳"。
   - **忽略输入文件里「输出：只输出表格 + 一行合计」那句**，那是旧模板遗留；按 `AUDIT_CONTRACT.md §四`：戳行 + 表头 + 16 行判定 + 合计行。
   - **表头照抄契约 §四**，不要用输入文件第 10 行那份简化表头（两者字不一样）。
4. 审计员权限只覆盖本批输入与本批输出；它读不到卡片、读不到别的批次，也不要给它贴卡片内容——**闭卷**是这套东西唯一的价值。

## 验收（每批返回后逐条过）

| # | 检查 | 判据 |
|---|---|---|
| 1 | 调用状态 | `completed`（若为空 `task_result` 但文件合规，按 RUNBOOK §三 视为通过） |
| 2 | 输出被覆盖 | `out_B{n}.md` 首行是戳行；匹配 `^\| B{n}-\d\d \|` 的**判定行恰好 16 条**；末尾有合计行。**不要数文件总行数**——现有 `out_B1.md` 是 20 行（表头 2 + 判定 16 + 空行 + 合计），加戳行后是 21 行，写「行数 = 16」会误判失败 |
| 3 | 戳一致 | 首行 `> 快照 sha1: <10 位>` 与输入文件第 6 行逐字相同，不带任何附加说明 |
| 4 | 合计行 | 表内条数与末尾「合计：16 条（...）」自洽；`audit-count` 能解析 |
| 5 | 路径 | 只写了 `out_B{n}.md`，没有碰卡片、契约、别的批次 |

三批都完成后：

```bash
python litrev/litrev.py audit-count --check    # 退 0，并贴出新的汇总数字
python litrev/litrev.py audit-stale --check    # 必须退 0
```

两条都绿，才可以写「131 条判定有效」。**不要**在主控侧就地改 `out_*.md` 的判定去凑 `audit-stale` 归零——那是伪造证据。

## 禁止事项

- 不改 `litrev/_probe/full/*.md`（卡片）、不改 `AUDIT_CONTRACT.md`、不改 `litrev/litrev.py`、不改 `.opencode/agents/` 下带 `AUTO-GENERATED` 的文件。
- 不新增/删除审计条目：条目集合由卡片决定，`batch` 负责同步，人不要手改。
- 不跑**不带参数**的 `batch`（输入已是最新，再跑只会制造无意义改动）；`batch --check` 是开工自检，不写盘，可以跑。
- 不跑 `stamp-out` 给 B1–B3 补戳：输入在判定后被改过，git 证明不了，硬补就是伪造证据。

## 做完写什么

`reports/round-04-reaudit.md`：

- 三批的 `task id`、子会话 id、`task_result` 是否为空；
- `audit-count` 与 `audit-stale` 的原始输出（不是转述）；
- 新旧判定差异表（哪条从 X 变 Y），以及因此变化的 131 条汇总；
- 仍然缺什么（例如 SUPPORTED 抽检尚未重做——卡片改过，`SAMPLE_S1` 已失效，需要重新 `sample`）。
