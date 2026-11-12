# Litreview · 新用户上手指南

> **这套系统做什么**：把「文献里的一句话能不能支撑综述里的一个论断」变成一条**可机械复核的证据链**——谁抽的、抽自哪一页、裁判怎么核、谁判的、能不能引用。
>
> **它不做什么**：不写综述正文，不判论文学术价值，不是「丢 PDF 进去自动出结果」的全自动流水线。产出是**卡片 + 判定表 + 批次报告**，供人决策。
>
> 本文只讲**怎么用 OpenCode 子代理系统**。改仪器、补证据的完整规程在 `RUNBOOK.md`；生产期的放行门槛在 `PRODUCTION.md`；当前进度与口径在 `PROGRESS.md`。三者与本文冲突时，以它们为准，并回来修本文。

---

## 零、三句话建立心智模型

1. **三层分工，不能合并**：**人**做派发、重启、开卷抽检、口径决策；**OpenCode 子代理**做抽取与判定；**`litrev.py`** 是裁判（子代理一律不可改）。主控（`orchestrator`）不亲自写卡片、不亲自改判定码。
2. **子代理是「文件级隔离的工人」，不是聊天助手**。每篇文献一个 `ex-`/`qx-` agent，权限按**路径**写死：只能读自己那篇 `txt`、只能写自己那张卡片。派它去碰隔壁文件会被拒——**被拒是隔离生效，不是 bug**。
3. **OpenCode 1.18.25 桌面客户端，无 CLI**。所有派发都在客户端对话里完成；**新增 agent 只在客户端启动时进注册表**，所以每次生成新 agent 后必须重启，否则报 `Unknown agent type`。

---

## 一、clone 之后第一件事：先看懂「缺了什么」

```bash
git clone https://github.com/qianluxi/Litreview.git
cd Litreview
pip install pymupdf          # index / text 必需
# pip install openpyxl       # 只在用 litrev.py matrix 时需要
python --version             # 开发/实测环境：Python 3.13.14
```

> **版权语料不入库**（`.gitignore` 明确排除）：`参考文献原文/*.pdf`、`litrev/_probe/texts/`、`litrev/_index/corpus.json.gz`。
> 这是刻意的——它们是已发表论文正文的完整复制。**新用户必须自备 PDF**。

我用一次全新 clone 实测过，落盘后是这样的：

| 目录 | clone 后 | 说明 |
|---|---|---|
| `.opencode/agents/*.md` | **67 个已在** | 子代理定义入库，可直接看 |
| `litrev/_probe/full/*.md` | **64 个已在** | 卡片（含引文短句）入库 |
| `litrev/_probe/audit/*.md` | 91 个已在 | 批次输入、判定输出、三份参考集、抽检留痕 |
| `参考文献原文/*.pdf` | **0** | 需自备 |
| `litrev/_probe/texts/*.txt` | **0** | 需由 PDF 重建 |
| `litrev/_index/corpus.json.gz` | **0** | 需由 PDF 重建 |

此时 `python tools/check.py` 是 **10/13**（不是全绿）：

| 红项 | 原因 | 要不要慌 |
|---|---|---|
| `verify 全库` | 没有 `corpus.json.gz`，32 张卡片的引文无处回查 | **不要**——这正是「缺语料」的正常表现 |
| `gen_subagents --check` | 报「缺少正文目录」，生成器靠 `texts/` 发现文献 | 同上 |
| `audit_prep sample S2 --check` | **已定案的永久红项**（`B2-08` 换过引文，冻结参考集复算不一致） | **永远不要修**；`batch_gate.py` 已把它列为豁免 |

其余 10 项（含 `card-check 32/32`、`audit-count 214 条`、`audit-stale 214/214`、`batch --check`、金标准／判例集）**全绿**——说明判定表、卡片结构、卡片↔批次对账这些**不依赖 PDF 的部分是可直接读的**。

### 按你的目的选一条路

| 目的 | 要做什么 | 能不能跑门禁 |
|---|---|---|
| **A. 只想看懂系统** | 读 `AGENT_ROLES.md` → `AUDIT_CONTRACT.md` → 任意一张 `full/*.md` + 对应 `out_R*.md`；跑 `audit-count`、`card-check` | 只需上面那 10 项绿 |
| **B. 想跑全库门禁** | 把**全部 40 篇**可用 PDF 放回 `参考文献原文/` → **先隔离拒收件**（§二 步骤 0）→ 重建 | 才能到 12/13 |
| **C. 想跑自己的新批次** | 至少要放本批 PDF；但 `batch_gate.py` 依赖 `check.py` 非豁免项全绿，**语料不全时会 `EXIT=1`** | 见 §五的诚实说明 |

> **一个容易踩的坑**：`python litrev/litrev.py index` 是**清空重建**，从 PDF 目录重新生成 `manifest.csv`。
> 仓库里入库的 `manifest.csv` 记着全部 40 篇可用文献；只放几篇 PDF 就跑，它会缩到几篇，已有卡片的引文就查不到了。
> 所以：**要么放齐，要么别跑全库门禁**，不要「先放几篇试试」。

---

## 二、重建语料（只在走 B/C 时做）

### 步骤 0 · 先把拒收件隔离出去（**漏了这步会停在 11/13**）

`index` 只扫描 `参考文献原文/*.pdf`（顶层），`text` 也会为顶层**每一篇**生成 txt。所以文字层不可用的 PDF 必须移进子目录：

```bash
mkdir -p 参考文献原文/_rejected
# 把符号串乱码、双栏交错、数字拆断的拒收件 move 进去，不要删（留作证据）
```

**为什么这是硬要求**：`tools/gen_subagents.py` 的 `slugify()` 只保留 `[a-z0-9]`。
**纯中文文件名归一后是空串**，两篇以上同时留在顶层就会撞名，生成器直接 `sys.exit`：

```
[!] 文件名主干归一后撞名：某围填海项目护岸地基处理方案研究-沈学明 与
    华南地区围填海项目高压旋喷桩地基处理工艺试验及研究-陆达仁，先改名
```

这也是「PDF 文件名必须是 `AuthorYYYY_ShortTag.pdf`（ASCII 开头）」的真实原因——不只是为了引文标注好看。

> 本仓库已把 4 个拒收件移入 `_rejected/` 并在 `.gitignore` 排除；`manifest.csv` 从 44 行降到 **40 行**，
> **已有 40 条零变化**，`gen --check` 仍 67/67。你自己新增文献时，拒收件也照此处理。

### 步骤 1 · 抽取与建索引

```bash
# PDF 放进 参考文献原文/，文件名必须是 AuthorYYYY_ShortTag.pdf
python litrev/litrev.py text --dry-run        # 文字层健康度，先看一眼
python litrev/litrev.py text                 # 生成 texts/*.txt（默认 --layout 词级坐标重建）
python litrev/litrev.py index                # 生成 corpus.json.gz + manifest.csv

# 生成子代理定义并核对同步
python tools/gen_subagents.py
python tools/gen_subagents.py --check        # 期望「✓ 同步：N 个文件与 AGENT_ROLES.md 一致」

# 验收
python tools/check.py
```

**这条链是实测过的**（2026-11-12，用一份全新 clone）：

| 阶段 | `check.py` | 红项 |
|---|---|---|
| 刚 clone | **10/13** | `verify`（无 corpus）、`gen --check`（无 texts）、`sample S2`（永久豁免） |
| 放齐 44 篇（**含 4 个拒收件**）、跑完三步、**没做步骤 0** | **11/13** | `gen --check` 撞名 + `sample S2` |
| 隔离 4 个拒收件、重跑 `index` | **12/13** | 只剩 `sample S2`（已定案豁免） |

**12/13 就是这套系统的正常绿态**，不是「还差一项没修」。

**PDF 文件名就是引文标注**：`Cao2025_SeismicSite_Reclamation.pdf` → `(Cao, 2025, p.3)`。同姓不同年靠年份区分；别名映射在 `litrev/aliases.json`。取不到作者/年份的文献，生成器会**跳过并打印原因**，不会静默出错。

**入库验收判据**（进批次前的第一道筛子，详见 `PRODUCTION.md §二·二`）：

1. **字符本身得是字**（前提）——若正文是 `!" #$%&'` 这类符号串，字体缺 `ToUnicode`，工具**没有 OCR 通道**，直接拒收；
2. **能不能从正文抄出一句连续的话**（主判据）——双栏交错会把一句切成三截，这种 `verify` 会 PASS（每个字都真实）但句不是作者写的；
3. **词/行不是判据**——实测拒收件的词/行 8.80 反而高于收下的三篇。

---

## 三、系统是怎么搭起来的

```
litrev/_probe/AGENT_ROLES.md   ← 唯一来源（人写）
          │  tools/gen_subagents.py 解析 ## ROLE: 段落，替换 {{占位符}}
          ▼
.opencode/agents/*.md          ← 生成物（67 个，带 AUTO-GENERATED 头，不要手改）
          │  opencode.json 指定 default_agent: orchestrator, subagent_depth: 1
          ▼
    OpenCode 桌面客户端启动 → 注册 → 对话里用 task 派发
```

| 角色 | 名字形态 | 能读 | 能写 |
|---|---|---|---|
| 主控（primary） | `orchestrator` | 映射表、规约 | 不写卡片、不判断定 |
| 首次抽取 | `ex-<文献slug>` | 自己那篇 `txt` + 契约 | **只创建**自己那张卡（`full/`） |
| 返工扩句 | `qx-<文献slug>` | 同上 | **唯一**能改写已存在卡片 |
| 批次审计 | `auditor-<批次>` | 契约 + 本批输入 | **只写**本批输出（闭卷） |
| 引文核验 | `checker` | — | 唯一被授权跑 `litrev.py verify/matrix/locate` |

> **clone 后查 `AGENT_MAP.md` 会发现 0 个 `ex-`、全是 `qx-`**，这是正常的：`ex-` 只在**卡片还不存在**时才生成（它只有创建权限，给已有卡片派它等于撞墙）。放新 PDF 之后才会出现对应的 `ex-`。

**为什么必须按文件生成、不能手写几份通用 agent**：权限是按相对 worktree 路径生效的（`edit`/`task` 都是**最后命中规则生效**）。要让「一篇文献一个工人且只碰自己那一个文件」成立，提示词里的路径必须和权限里的路径逐字相同——手写 20 多份必然漂移，生成是唯一能保证的办法。

**为什么有的工具「拿不到拒绝原文」**：`visibleTools` 用 `findLast`，若 `pattern==="*" && action==="deny"`，工具**根本不注册**。所以 `auditor` 的 `bash: "*": deny` 不是「调用被拦」，是「它没有 bash 这个工具」。只有部分 allow 时才会暴露工具、调用时抛 `PermissionDeniedError`。

**改角色规则的唯一正确姿势**：改 `AGENT_ROLES.md` → 跑 `gen_subagents.py` → `--check` → **重启客户端**。手改生成物会被 `--check` 抓出，并在下次生成时覆盖。

---

## 四、一次完整批次（照着做，共 3 次交互）

> 下面用「P3 = 新放 N 篇 PDF」举例。命令里的批次名要按实际续号改（`R9`/`R10` 之后是 `R11`）。

### 交互 1 · 人放 PDF → 主控验收入库

主控做：按 §二 的判据逐篇验收（收/拒）→ 改名 `AuthorYYYY_ShortTag.pdf` → 登记 `aliases.json` → `text` / `index` / `gen_subagents.py` → **写一份 `HANDOFF-NN.md`**（内含逐篇陷阱、现成派发词、事前预测）。

**然后人重启 OpenCode 客户端**（新 `ex-` agent 要注册）。

### 交互 2 · 人派抽取 → 主控验收 + 建批次

在**同一条消息里并列**发多个 `task`（不要串行）：

```
按 HANDOFF-27.md §五 的要求，用 ex-<文献slug> 抽取 <文献名> 这篇文献，产出 7 节卡片。
```

子代理回来后，主控**只认文件不认回话**（`completed` ≠ 成功，空 `task_result` 是已知现象）：

```bash
python litrev/litrev.py card-check --only <文献名>
python litrev/litrev.py verify litrev/_probe/full/<文献名>.md
```

7 节固定：**一句话主张 / 问题域 / 案例或数据的表示形式 / 相似性或检索机制 / 系统形态 / 评价方式 / 明确写出的局限**（节名字、编号、顺序一字不改）。原文确实没写的节写 `- 论断：未涉及` 且**不留引文行**。

然后建批次：生成 `REST_B11.md`（N 条）→ 在 `litrev/_probe/audit/BATCHES.json` 追加一条 → 跑 `python litrev/litrev.py batch --only B11` 写戳 → 跑 `gen_subagents.py` 生成 `auditor-rest-b11` → **人再重启一次**。

> 此时 `check.py` 会红 6 项（`audit-stale` + 5 个参考集「只在输入」）。**这是备料态，不要修、不要补占位 `out_*.md`、不要重抽参考集**；判定回来且戳同源就自愈。

### 交互 3 · 人派判定 → 主控验收 + 抽检 + 出报告

```
按 HANDOFF-27.md §六 做 N 条判定，用 auditor-rest-b11 这个子代理。
```

派发词里必须写死三件容易错的事：表头**逐字照抄本次输入文件**、依据列 ≤15 字且是引文内连续片段、**首行 `> 快照 sha1: …` 原样抄到输出头部**（戳抄错整批重来）。

```bash
python litrev/litrev.py audit-stale --check      # 依据与卡片一致
python litrev/litrev.py audit-count              # 口径（唯一来源，不许手算）
```

然后**人开卷抽检**（这一步不能省、不能交给子代理）：支撑轴 `SUPPORTED` 池随机抽 ≥20%，回原文看前后段，写 `SAMPLING_R11.md`。最后一条命令出报告：

```bash
python tools/batch_gate.py --batch rest_b11 --date 2026-11-12 \
  --note "<第 4 行的人话处置结论>" --write --out reports/batch-2026-11-12-P3.md
```

`EXIT=0` 才可交付；`1` 门禁未过 / `2` 抽检记录不全 / `3` 熔断。报告前三行由脚本生成，**一个字符都不许手写**。

---

## 五、人必须做的四件事（别想交给 agent）

| 事 | 为什么不能交给 agent |
|---|---|
| **派发** | 主控 `orchestrator` 是 primary，**实测无权限层**（`opencode.json` 只 deny 了 `webfetch`/`websearch`）。靠自律不靠机制，所以派发必须人做。 |
| **重启客户端** | 机制约束，不是流程设计。新 agent 只在启动时注册。 |
| **开卷抽检** | 检的是「引文有没有被断章取义」，闭卷判不了；且金标准实测支撑轴漏判 ~13%、方向偏松，这是唯一会放行错误论断的轴。 |
| **口径决策** | 契约留白、争议条目（`DISPUTED.md`）、改不改稿，都是人的裁决，不是机器的多数票。 |

**一句实话**：金标准人开卷 vs 机器闭卷，支撑轴一致 13/15、自足轴 15/15。所以系统的形态是**机器 + 抽检**，不是全自动。抽检由「同一台仪器第二遍」执行时，独立性弱于真人开卷——交给别人用时，建议每批由他随手抽 2 条自己看。

---

## 六、坑速查表

| 现象 | 原因 | 动作 |
|---|---|---|
| `Unknown agent type` | 没重启客户端 | 重启，别改 agent 名 |
| `task` 返回 `completed` 但 `task_result` 空 | OpenCode 已知现象（实测 8 次 3 次） | **看交付文件**；文件合规即通过，别重派（会产生第二份不一致结论） |
| 工具「不存在」而不是「被拒绝」 | `visibleTools` 全量 deny → 工具根本不注册 | 设计使然，不是授权缺口 |
| 备料态 6 项红 | `out_<批次>.md` 还没回来 | **不要修**、不要补占位文件 |
| `audit-stale` 报依据不一致 | 卡片改过但判定没跟着改 | 走 `reseal` 三门槛，别手工改戳 |
| `out_P6.md` 污染口径 | `audit-count` 正则 `^out_[A-Z]+\d+\.md$` 会命中 | 探针输出写 `out_P_6.md`；`out_FIX5.md` 同理 |
| `gen_subagents.py` 报「文件名主干归一后撞名」 | 顶层同时留了两篇以上**纯中文名** PDF，`slugify` 后都是空串 | 移进 `参考文献原文/_rejected/`、删对应 txt、重跑 `index`（§二 步骤 0） |
| 手改了 `.opencode/agents/*.md` | `--check` 会报「与模板不一致」 | 跑 `gen_subagents.py` 覆盖（改规则请改 `AGENT_ROLES.md`） |
| 用关键词断言「原文没写」 | 正则漏词形变化（实测 `similarit` 漏 `similar`，错 2 篇） | 断言「没有」要覆盖词形变化——它不出现在任何输出里，没人会复核 |
| `verify` 报 `MISSING` 但引文看着一样 | 归一化差异（`norm_text` 走 NFKC） | 全角数字照抄即可 PASS；**内容真不一致时不许改引文凑** |

**绝对不要动**：`litrev/litrev.py`（裁判）、契约判定条款、`litrev/_probe/full/` 里已封戳批次的卡片。改稿只有两种合法动作：情态降回原文强度、删掉引文里没有的成分；且要走 `FIX_B*` 定点重判 + `reseal`。

---

## 七、文档地图

| 想找什么 | 读哪个 |
|---|---|
| 本文（怎么上手、怎么派活） | `README.md` |
| 生产期：每批门禁、抽检比例、熔断、不许报的数字 | `PRODUCTION.md` |
| 标定期：派发协议、验收五条、reseal、参考集、权限回归 | `RUNBOOK.md` |
| 当前进度、口径、对外说法 | `PROGRESS.md` |
| 子代理提示词的唯一来源 | `litrev/_probe/AGENT_ROLES.md` |
| 论断判定的唯一标准（v1.2） | `litrev/_probe/AUDIT_CONTRACT.md` |
| 文献 → agent 名映射（派活前必查） | `litrev/_probe/AGENT_MAP.md` |
| 有哪些批次、输入输出在哪 | `litrev/_probe/audit/BATCHES.json` |
| 未决争议（按 `D-0x` 编号） | `litrev/_probe/audit/DISPUTED.md` |
| 本批派发词、逐篇陷阱、事前预测 | 最新的 `HANDOFF-NN.md` |
| 历次变更事实（按日期倒序追加） | `RUNBOOK.md §八` |
| 已交付批次报告（四行模板） | `reports/batch-*.md` |

> **数字会过期**：本文与规程里的示例数字（`S166`、`n=21`、`166/166` 等）多是写规程当时的读数。
> **任何时候报口径，以 `python litrev/litrev.py audit-count` 的当次输出为准**，不要从文档里抄。

---

## 八、自检：下面几条答不上来，先别派活

1. 新放了 3 篇 PDF，也跑了 `gen_subagents.py`，能直接派 `ex-` 吗？→ **不能，先重启客户端**。
2. 建完批次看到 `check.py` 红 6 项，要修吗？→ **不要，那是备料态**。
3. 子代理返回 `completed` 但回话是空的，算成功吗？→ **看文件**；文件合规才算，且不要重派。
4. `card-check` 全绿、`verify` 全绿，就能说这一批没问题吗？→ **不能**。`verify` 只查引文逐字存在，`card-check` 只查结构；「论断有没有超过引文」靠审计支撑轴，「这节答的是不是这节问的事」只能人读卡片。
5. `verify 214/214` 能证明仪器在陌生文本上能抓错吗？→ **不能**，卡片是照着引文改到对上的。灵敏度看金标准（支撑 13/15）。
6. 全新 clone、放齐 PDF、`text`/`index`/`gen` 都跑了，门禁就全绿了吗？→ **不，是 11/13**；还要把拒收件隔离进 `_rejected/` 才是 12/13。而且 **12/13 本身就是正常绿态**（`sample S2` 永久豁免）。

---

## 附：本文对应的状态快照

- 日期：**2026-11-12**，commit `ec08ce7`（已推 `main`）
- 判定表：**214 条 · `S208/P6/U0` · `SELF181/DEP33`**
- `check.py`：**12/13**（唯一红项 `sample S2` 为已定案豁免）
- 语料：顶层可用 PDF **40 篇**，`_rejected/` 拒收 **4 篇**（不入库）
- 已交付批次：**P1**（中文围填海 18 条）、**P2**（英文围填海 30 条）
- 子代理：**67** 个（`gen --check` 67/67）

这些数字只用于让你判断「读到的是不是当前版本」，不是指标。最新值永远以 `audit-count` 为准。
