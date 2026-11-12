# Litreview · 新用户上手指南

**这套系统做什么**：把「文献里的一句话能不能支撑综述里的一个论断」变成一条可机械复核的证据链——谁抽的、抽自哪一页、裁判怎么核、谁判的、能不能引用。

**它不做什么**：不写综述正文，不判论文学术价值，不是「丢 PDF 进去自动出结果」。产出是**卡片 + 判定表 + 批次报告**，供人决策。

> 本文只讲最短上手路径。改仪器、补证据 → `RUNBOOK.md`；生产放行门槛 → `PRODUCTION.md`；口径与进度 → `PROGRESS.md`。三者与本文冲突时以它们为准。

---

## 一、你要做的 5 步

| # | 你做什么 | 系统里发生什么 |
|---|---|---|
| **0** 准备（一次） | `git clone` → `pip install pymupdf` → **自备 PDF** | 版权语料不入库（`.gitignore` 排除 `参考文献原文/` 下所有 PDF、`texts/`、`corpus.json.gz`），clone 后这三样是空的 |
| **1** 放文献 | 新 PDF 放进 **`参考文献原文/<库名>/`**（一个用户 / 一个批次一个库），命名 `AuthorYYYY_ShortTag.pdf`；定不了名的可写 `_names.txt` 清单（见下） | 现有 40 篇调试基线在 `0号文献库`。文件名就是引文标注：`Cao2025_X.pdf` → `(Cao, 2025, p.3)`；别名写 `litrev/aliases.json` |
| **2** 一键准备 | **双击根目录 `准备文献库.bat`**，按提示回车/定名 → **人重启 OpenCode 客户端** | 向导自动跑完整个机器侧：全库预检 → 命名 → 文字层体检 → `index` 全库重建（已有条目零变化校验，异常自动回滚）→ `text --library` → 生成 `ex-` → `gen --check`；结束时直接打印本次可派的 `ex-` 名字 |
| **3** 派抽取 | 在客户端**同一条消息里并列**派 `ex-<文献slug>` → 主控验卡、建批次 → **再重启一次** | 每篇产出一张 7 节卡片；生成 `REST_B*.md` 批次输入和 `auditor-<批次>` |
| **4** 派判定 + 抽检 | 派 `auditor-<批次>` 出判定 → **人开卷抽检 ≥20%** 支撑轴并写 `SAMPLING_*.md` | 逐条给出支撑 / 自足两轴结论；抽检不能交给子代理 |
| **5** 放行 | 跑 `batch_gate.py` 出批次报告 | `EXIT=0` 才可交付；`1` 门禁未过 / `2` 抽检记录不全 / `3` 熔断 |

**向导会问什么**（全部合规时只需一次确认回车）：

- 选本次入库的库（只有一个新库时自动选）；
- 逐篇给不合规 PDF 定名：`a` 采纳工具建议 / 直接输入 `Smith2024_ShearWall` / `s` 暂不入库（移到 `_parked/`）/ `q` 中止（此时未改任何文件）；
- 其它库里还留着不合规的新 PDF 时，问是否**临时隔离**：目录名前加 `_`，不删文件、随时改回；
- 重建索引前最后确认一次。`--plan` 参数可先做只读预检，不写盘、不改名。

想把逐篇定名前置掉，就在该库放一份 `_names.txt`（`#` 开头是注释）：

```text
downloaded_v2.pdf=Smith2024_ShearWall
某篇原名.pdf=Higgins2013_PalmJumeirah
```

清单只覆盖该库待定名的文件；格式不对、撞名、对不上原名的行会被忽略并提示。年份要开卷核实（期刊页/版权页），工具不替你猜。

> **文字层只做了机械预检**（`wpl < 3`）。`PRODUCTION.md §二·二` 的人眼判据（先看字符可读性、再看句子连续性）仍然要人做，向导不替代。

```bash
# 排障时才用：手工等价命令（正常走 bat）
python tools/prepare_library.py --plan          # 只读预检
python tools/rename_pdfs.py --library <库名>    # 只看不改的命名建议
python litrev/litrev.py text --library <库名> --dry-run
python litrev/litrev.py index                  # 始终全库清空重建，PDF 不全时别跑（见 §四）
python litrev/litrev.py text --library <库名>
python tools/gen_subagents.py && python tools/gen_subagents.py --check

# 步骤 3 验卡 / 步骤 4 验收
python litrev/litrev.py card-check --only <文献名>
python litrev/litrev.py verify litrev/_probe/full/<文献名>.md
python litrev/litrev.py audit-stale --check
python litrev/litrev.py audit-count          # 口径的唯一来源，不许手算、不许抄文档

# 步骤 5
python tools/batch_gate.py --batch rest_b11 --date 2026-11-12 \
  --note "<人话处置结论>" --write --out reports/batch-2026-11-12-P3.md
```

**一次完整批次 = 3 次人机交互**：人放 PDF → 派抽取 → 派判定，中间各重启一次客户端。批次名按实际续号改（`R9`/`R10` 之后是 `R11`），派发词照最新的 `HANDOFF-NN.md` 抄。

> **重启是机制约束**：OpenCode 1.18.25 桌面版无 CLI，新 agent 只在客户端启动时进注册表，不重启就报 `Unknown agent type`。

**派发词里必须写死三件事**：表头逐字照抄本次输入文件；依据 ≤15 字且为引文内连续片段；首行 `> 快照 sha1: …` 原样抄到输出头部（戳抄错整批重来）。

---

## 二、最后你会得到什么

| 产物 | 在哪 | 内容 / 用途 |
|---|---|---|
| **文献卡片** | `litrev/_probe/full/*.md` | 每篇 7 节（一句话主张 / 问题域 / 表示形式 / 相似性或检索机制 / 系统形态 / 评价方式 / 明确写出的局限）。每节一句论断 + 0 或 1 条**逐字引文带页码**；原文没写的节写 `- 论断：未涉及` 且不留引文行。节名、编号、顺序不可改 |
| **批次输入 + 判定输出** | `litrev/_probe/audit/REST_B*.md`、`out_R*.md` | 每条论断两轴结论：支撑 `SUPPORTED / PARTIAL / UNSUPPORTED` × 自足 `SELF / DEPENDENT`，附依据片段。这就是「这句能不能这么写」的逐条裁决 |
| **判定表总账** | `python litrev/litrev.py audit-count` | 全库条数与两轴分布，唯一口径来源。文档里的示例数字会过期，任何时候以当次输出为准 |
| **批次报告** | `reports/batch-*.md` | 脚本生成的四行：门禁状态 / 抽检 / 偏松条数 / 人话处置结论。**前三行一个字符都不许手写** |

**物理布局**：`manifest.csv` 的 `library` 列记着每篇 PDF 属于哪个库；`corpus` 仍以**文件名**为键，所以把 PDF 移到别的库不会改变引文标注（实测 40 条零变化）。跨库同名会被 `index` 直接拦下。

**拿去怎么用**：`SUPPORTED + SELF` 且经抽检的条目，是可以直接写进综述的「论断 ↔ 引文 ↔ 页码」对，且随时能机械复核；`PARTIAL` 要改稿或不用（生产期不改稿，如实留表）；`DEPENDENT` 表示引文脱离上下文读不懂，引用时要补主语或补上下文。

**不会得到**：一篇写好的综述、对论文质量的评价、100% 正确的自动判定。金标准实测人开卷 vs 机器闭卷支撑轴一致 **13/15**、自足轴 **15/15** —— 这是**机器判定 + 人开卷抽检**的系统，不是全自动。

**正常绿态**：`check.py` **12/13**（唯一红项 `sample S2` 是已定案永久豁免，`B2-08` 换过引文；**变绿反而要查**），`gen --check` 67/67。刚 clone 只有 10/13 是缺语料的正常表现，不是故障。

---

## 三、四件不能交给 agent 的事

| 事 | 原因（一句） |
|---|---|
| **派发** | 主控 `orchestrator` 是 primary，实测无权限层，靠自律不靠机制 |
| **重启客户端** | 机制约束，不是流程设计 |
| **开卷抽检** | 检的是「引文有没有被断章取义」，闭卷判不了；支撑轴是唯一会放行错误论断的轴 |
| **口径决策** | 契约留白、争议条目（`DISPUTED.md`）、改不改稿，都是人的裁决，不是机器的多数票 |

---

## 四、最容易踩的坑

| 现象 | 动作 |
|---|---|
| `Unknown agent type` | 重启客户端，别改 agent 名 |
| 子代理返回 `completed` 但回话为空 | **只看交付文件**；文件合规即通过，别重派（会产生第二份不一致结论） |
| 建完批次 `check.py` 红 6 项 | **备料态，不要修**、不要补占位 `out_*.md`、不要重抽参考集；判定回来且戳同源就自愈 |
| 工具「不存在」而不是「被拒绝」 | `visibleTools` 全量 deny 时工具根本不注册，设计使然 |
| `gen_subagents.py` 报「文件名主干归一后撞名」 | 同一库里留了两篇以上纯中文名 PDF（`slugify` 后都是空串）→ 移进 `参考文献原文/_rejected/`、删对应 txt、重跑 `index` |
| `index` 报「跨文献库同名 PDF」 | 两个库放了同名文件，corpus 会互相覆盖 → 先给其中一份改名 |
| `rename_pdfs.py` 出 `REVIEW` | 抽不出 ASCII 作者/年份/题名（常见于中文文献），或元数据只是 Word 模板 / 出版社书名残留 → 别让它猜，照首页正文用 `--set "原名.pdf=AuthorYYYY_Tag"` 人工定名后再 `--apply` |
| `index` 只放了几篇 PDF | 它是**清空重建** `manifest.csv`，已有卡片引文会查不到 → 要么放齐全部库，要么别跑全库门禁 |
| 向导报「其它库还有不合规新文件」 | 选**临时隔离**（目录改名 `_<库名>`）；别跳过，否则坏名会被 `index` 写进 `manifest.csv`。要恢复就去掉前缀 |
| `_parked/` 里出现 PDF | 是你在向导里选了「暂不入库」，不参与扫描、文件没删；`_rejected/` 才是文字层坏件的隔离区 |
| 双击 bat 后窗口一闪而过 | 用命令行跑一次 `准备文献库.bat --plan` 看报错；无参数双击时窗口会 `pause` 停留 |
| 向导报「统计列重算漂移」，或旧版报「index 动了已有条目」 | 多半是 bat 的解释器 PyMuPDF 版本与索引基准不同（实测 **1.28.2 vs 2.0**，词/行 4.26→4.35），**不是 PDF 被换**；现在由 `verify 全库` 裁决，全绿即放行。想完全对齐旧基准：`set LITREV_PYTHON=<基准 python.exe>` 后再双击 |
| `index` 报「无文字层 / 逐词断行 / 内容重复」 | 那是 `0号文献库` 40 篇基线里的历史遗留，每次全库重建都会报；`gen_subagents.py` 会跳过它们、不给它们派 `ex-`，**不影响新库**。要清就把文件移进 `_rejected/` 再重跑向导 |

**绝对不要动**：`litrev/litrev.py`（裁判）、契约判定条款、`full/` 里已封戳批次的卡片。改稿只有两种合法动作（情态降回原文强度、删掉引文里没有的成分），且必须走 `FIX_B*` 定点重判 + `reseal`；卡片改过但判定没跟上时用 `audit-stale` 查，**别手工改戳**。

> 探针输出命名：`audit-count` 正则 `^out_[A-Z]+\d+\.md$` 会误收 `out_P6.md` / `out_FIX5.md` → 写成 `out_P_6.md` / `out_FIX_5.md`。

---

## 五、按需再读

| 想找什么 | 读哪个 |
|---|---|
| 生产期每批门禁、抽检比例、熔断 | `PRODUCTION.md` |
| 一键准备向导的参数 / 只读预检 | `python tools/prepare_library.py --help`、`--plan` |
| PDF 自动命名建议、改名留痕 | `tools/rename_pdfs.py`（默认 dry-run） |
| 派发协议、验收五条、`reseal`、参考集、权限回归 | `RUNBOOK.md`（§八 按日期倒序记录变更） |
| 子代理提示词唯一来源 / 判定唯一标准 | `litrev/_probe/AGENT_ROLES.md` / `AUDIT_CONTRACT.md` |
| 文献 → agent 名映射（派活前必查） | `litrev/_probe/AGENT_MAP.md` |
| 本批派发词、逐篇陷阱、事前预测 | 最新的 `HANDOFF-NN.md` |
| 未决争议 | `litrev/_probe/audit/DISPUTED.md` |

改角色规则的唯一姿势：改 `AGENT_ROLES.md` → `gen_subagents.py` → `--check` → **重启客户端**。手改 `.opencode/agents/*.md` 会被 `--check` 抓出。

---

**状态快照（2026-11-12）**：判定表读数以 `python litrev/litrev.py audit-count` 为准（唯一可信来源）；下面两行只用来判断读到的是不是当前版本，**不是指标**。

| 版本 | 判定表 | 门禁 | 文献库 | 子代理 | 已交付批次 |
|---|---|---|---|---|---|
| 上次推送基线 `de80dfe` | 214 条 · `S208/P6/U0` · `SELF181/DEP33` | `check.py` 12/13 | `0号文献库` 40 篇 + `_rejected/` 4 篇（均不入库） | 67 | P1（18 条）、P2（30 条） |
| 本次提交（P3 收口） | **237 条 · `S231/P6/U0` · `SELF203/DEP34`** | `check.py` 12/13 | 上述 + `DXS/` 6 篇 | 74 | P1、P2、P3（23 条） |
