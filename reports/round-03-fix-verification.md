# round-03 返工：第三方核验

- 核验对象：`reports/round-03-fix.md`（OpenCode 侧执行）与工作区实际状态
- 核验方式：不看报告结论，直接从 `~/.local/share/opencode/opencode.db` 取派发记录、重跑裁判、机械比对批次输入与卡片
- 时间：2026-11-09 21:00 前后

## 一、结论

| 项目 | 结果 |
|---|---|
| 3 处引文是否按指令落地 | **是**，逐字与给定文本一致 |
| `verify` 全库 | **131 PASS / 131 条**，0 PARAPHRASE / MISSING / PAGE / NOPAGE / AUTHOR |
| 派发是否真的发生 | **是**，3 次 `task` 全部 `completed`，子会话与报告所列 id 逐字一致 |
| 空 `task_result` | **0 次**，未触发恢复流程（报告 §五 属实） |
| 权限拒绝 | **1 次**：`checker` 跑 `audit-count` 被拒（白名单缺这条），已修 |
| 131 条判定的有效性 | **只有 111 条的依据仍然成立**，20 条过期（3 条本轮 + 17 条 T1 遗留） |

**一句话**：返工本身执行正确，但「131 条已审」这个口径仍然是虚的——`audit-count` 的数字漂亮，是因为它数的是判定表，不数判定所依据的引文是否还在。

## 二、派发取证（数据库，不是报告）

```
20:55:59  by=orchestrator  child=ses_e3f9ec8d3ffe2Gdv2calxVGlL5  status=completed  outlen=312
20:56:32  by=orchestrator  child=ses_e3f9e45abffe2s08YdqQGcCGEj  status=completed  outlen=387
20:57:16  by=orchestrator  child=ses_e3f9d9923ffeLlUmUrpLL6l1bu  status=completed  outlen=3139
```

- 三个子会话的 `agent` 分别是 `qx-zhang2006-...`、`qx-borner1993-...`、`checker`，父会话为同一个 `ses_e3fa01c0bffe...`（20:54:32 创建）。
- `outlen` 全部 > 0，与报告「三次均非空」一致。
- 拒绝 1 次，`checker` / `bash`，原文：

```
The user has specified a rule which prevents you from using this specific tool call.
[{"permission":"*","action":"allow","pattern":"*"},
 {"permission":"bash","pattern":"*","action":"deny"},
 {"permission":"bash","pattern":"python litrev/litrev.py verify*","action":"allow"},
 {"permission":"bash","pattern":"python litrev/litrev.py matrix*","action":"allow"},
 {"permission":"bash","pattern":"python litrev/litrev.py locate*","action":"allow"}]
```

报告里说「隔离生效，不是失败」——判断正确，但它没有权限跑汇总，导致主控补跑，破了「裁判只由 checker 跑」这条。**这条缺口已在本轮修掉**（见 §六）。

## 三、verify 复算

19 份卡片逐份重跑 `verify`，汇总相加：**PASS=131，总条数 131，其余判定码全为 0**。与报告 §2.1 一致。

报告 §四 D-1 指出我给的期望「132 PASS」是错的——**它对，我错**。原因值得记下来：

- `verify` 数的是**引文条数**（返工前 132：Borner 8 + Zhang 7 + 其余 117）；
- `audit-count` 数的是**判定表行数**（131，按「文献 × 节」一行）；
- 本轮 Borner §5 由 2 条删成 1 条（净 −2 +1 = −1），引文总数 132 → 131，所以上限就是 131，不是 132。

报告没有为了凑我给的数字去补引文，这是对的。但要注意：**这两个 131 是两件事，数字相同只是巧合**。真正的对应关系见下一节。

## 四、新发现：20 条判定的依据已经过期

`FRAG_B1/B2/B3.md` 冻结于 **14:15**，`REST_B1–B5.md` 冻结于 **14:29**；卡片在 **16:46**（T1 扩句 15 条）和 **20:55**（本轮 3 条）被改写。批次输入没有跟着变。

本轮新增 `litrev.py audit-stale`，按 `(文献, 节, 论断, 引文)` 四元组比对批次输入与卡片当前内容：

```
批次输入 131 条 · 卡片 19 篇 / 133 节 / 131 条引文
判定依据与卡片一致：111/131
```

过期 20 条，全部在 `FRAG_B1–B3`（`REST_B1–B5` 的 83 条**全部一致**）：

| 来源 | 条数 | id |
|---|---|---|
| 本轮改的 3 条 | 3 | B1-14（Zhang 局限）、B2-04（Borner 系统形态）、B3-12（Zhang 表示形式，**论断也改了**） |
| T1 扩句改过的 | 17 | B1-03/04/05、B1-12/13、B2-01/03/05/08/09/12/13、B3-02/03/04/13/16 |

判定「不算本轮引入」的依据：把 HEAD（`e8c140b`）版卡片导出来跑同一条命令，**同样是 20 条过期、同一份清单**。本轮在数量上中性。

但有一个更严重的事实：快照里的旧引文是**文本层坏掉的那一版**。例如 B2-04 的快照：

```
引文："Our approac h is protot ypically implemen ted in Synt erm" (Borner, 1993, p.8)
```

词内被插空格（`approac h` / `protot ypically`）。也就是说：

- **17:03 那次 `out_B1.md` 重审，重的是 14:15 快照里的旧引文**，不是重建语料后的新引文——那次重审等于白跑，而它现在仍被当作「B1 已复审」的依据。
- 「B3 重审后把 4 条旧 SUPPORTED 降为 PARTIAL」这类结论，同理需要重新核对它审的是哪一版文字。

所以本轮之后可以说的准确话是：**131 条引文全部逐字存在于原文；其中 111 条有与其当前文字相符的论断判定，20 条需要重审。**

## 五、本轮引入的两处问题（下一轮修）

### 5.1 Borner §5 论断与新引文不匹配 —— 我的指令造成的

| 项 | 内容 |
|---|---|
| 当前论断 | 该方法以原型形式实现于 SynTerm。 |
| 当前引文 | "SynTerm and SynGraph supply the system with solutions for special design problems" (p.9) |

新引文里没有「原型」「实现」任何字样，`PARTIAL` 起步。上一条 p.8 的「prototypically implemented」正是支撑这个论断的，我给的替换指令把它删了却没让改论断。

两个修法，**推荐 A**：

- **A（保持每节一条引文）**：论断改为「系统由 SynTerm 与 SynGraph 两个子系统构成，二者为系统提供专项设计问题的解法。」引文不动。代价是丢掉「原型实现」这条信息。
- **B（保住原型实现）**：§5 放两条引文 + 论断改为「该方法以原型形式实现于 SynTerm 与 SynGraph 两个子系统。」两条均已 `locate` 到 1.00：

```
"Our approach is prototypically implemented in SynTerm for Synthesis by using Term based knowledge representations"  (p.8)
"SynTerm and SynGraph supply the system with solutions for special design problems"                                  (p.9)
```

代价是**一节两条引文而判定表只给一行**——第二条不会被审计到。这也是当前 Liao/Sriram 的问题（见 §七）。

### 5.2 Borner §2 引文以 Both 起首

```
论断：系统面向工业建筑设计领域。
引文："Both are integrated in a knowledge based system which operates in the domain of industrial building design Whereas the overall system provides user interfaces and a broader range of functionality SynTerm and SynGraph supply the system with solutions for special design problems" (p.9)
```

三个问题：`Both` 作主语、指代对象在上一页（跨页，`verify` 也不接受跨页引文）；两句话被 PDF 挤成一句（`Whereas` 前无句点）；尾部与 §5 的新引文完全重叠，等于同一句证据用两次。

可替换（已 `locate` 1.00，p.1）：

```
"Although our approach is more theoretical in nature and not restricted to a speci c domain we will give an example taken from the domain of industrial building design"
```

论断相应改为「方法本身不限于特定领域；示例取自工业建筑设计领域」。**注意 `speci c` 是 Type3 连字丢失，必须原样抄，补成 `specific` 就变 PARAPHRASE。**

我上一轮把这条错算成 §5 的第三条引文（报告 D-2 记录了这一点，`qx-` 没照做是对的）。

## 六、本轮我方改动

1. `litrev.py` 新增 `audit-stale`（含 `--check`，过期即退出 1）。存在的理由：`audit-count` 只保证「判定表自己自洽」，不保证「判定对的是现在的文字」；这两天上过两次当，都是数字漂亮而依据已换。
2. `checker` 的 `bash` 白名单加 `audit-count` 与 `audit-stale`；`AGENT_ROLES.md` 的命令清单同步为五种，并写明「汇总只能照抄 `audit-count` 输出」「`audit-stale` 不为 0 时报告要写有效判定数，不许只写汇总」。`gen_subagents.py --check` 通过。

## 七、仍未解决

| 项 | 状态 | 影响 |
|---|---|---|
| 20 条过期判定 | 未重审 | 「131 条已审」不成立，只有 111 条 |
| Borner §5 论断/引文不匹配 | 未修（需 `qx-`） | 该条按现状至少 PARTIAL |
| Borner §2 `Both` 起首 | 未修（需 `qx-`） | 自足轴 DEPENDENT |
| Liao1998 / SriramMaherFenves1985 | 各 7 节 6 引文 | 各有一节无引文，配对检查不齐 |
| 批次输入无重建机制 | 靠手写 | 每次改引文都要重建，否则 `audit-stale` 只增不减 |

## 八、下一步顺序（建议）

1. **修 Borner 两处**：派 `qx-borner1993-...` 一次，§2 换句 + 改论断、§5 按 A 改论断（或按 B 加回 p.8）。
2. **重建过期批次**：`FRAG_B1/B2/B3` 按卡片当前内容重cut（48 条），派三个 `auditor-frag-b*` 重审；`REST_B1–B5` 不动（83 条全部一致）。
3. **验收**：`verify` 131 PASS、`audit-count --check` 退 0、`audit-stale --check` 退 0。三条同时绿，才可以说「131 条有效判定」。
4. 不要就地改 `out_*.md`：判定的可追溯性建立在「批次输入 → 输出」这份快照上，就地改会让历史判定无法复现。
