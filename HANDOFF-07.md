# HANDOFF-07：D-01 第三次判定 + B1–B3 双跑

> 本轮只做 4 个 task，全部基于**当前 v1.1 契约**（不改契约、不改判定表）。
> 目的：① 给 D-01（B3-10）补第三次独立判定，看它是漂移还是判错；② 补 B1–B3 的 frag 双跑，把双跑基线从 83 条扩到 131 条。
> **本轮不碰**：`out_B1..B3.md`、`out_R1..R5.md`、`out_D1..D5.md`、`out_S1.md`、`litrev.py`、`AUDIT_CONTRACT.md`。

## 一、前置核对（派活前逐条确认）

| 项 | 应见到 |
|---|---|
| 4 个新 agent 存在 | `.opencode/agents/auditor-frag-b3-probe.md`、`auditor-frag-b1-dup.md`、`auditor-frag-b2-dup.md`、`auditor-frag-b3-dup.md` |
| `gen_subagents.py --check` | 退 0（42 个文件同步） |
| B3P 输入戳（`FRAG_B3P.md` 第 6 行） | `e894bb155c` |
| B3P 输入条数 | 1 条（`^### B3-10`） |
| frag 输入条数 | B1=16、B2=16、B3=16（`^### B\d-\d\d`） |
| 输出文件派活前状态 | `out_B3P.md`、`out_E1.md`、`out_E2.md`、`out_E3.md` **均不存在** |

## 二、派发（顺序执行，一次一个，上一个返回后再派下一个）

| # | agent | 输出 | 条数 | 说明 |
|---|---|---|---|---|
| 1 | `auditor-frag-b3-probe` | `litrev/_probe/audit/out_B3P.md` | 1 | D-01 第三次独立判定 |
| 2 | `auditor-frag-b1-dup` | `litrev/_probe/audit/out_E1.md` | 16 | frag 双跑 B1 |
| 3 | `auditor-frag-b2-dup` | `litrev/_probe/audit/out_E2.md` | 16 | frag 双跑 B2 |
| 4 | `auditor-frag-b3-dup` | `litrev/_probe/audit/out_E3.md` | 16 | frag 双跑 B3 |

### 每个 task 的提示词（逐字照发，只改 agent 名与输出）

```
按 HANDOFF-07.md 执行本轮第 N 个 task，用 auditor-frag-b3-probe 这个子代理。
它只能读 litrev/_probe/audit/FRAG_B3P.md 和契约，只能写 litrev/_probe/audit/out_B3P.md。
首行原样抄输入文件里的「> 快照 sha1:」，表头照契约 §四，只输出表格 + 一行合计。
写完停下，报「已写入 out_B3P.md：N 条（...）」，不要做别的事。
```

第 2–4 个 task 把 agent 名、输入、输出、条数替换即可：
- B1：`auditor-frag-b1-dup` / `FRAG_B1.md` / `out_E1.md` / 16 条
- B2：`auditor-frag-b2-dup` / `FRAG_B2.md` / `out_E2.md` / 16 条
- B3：`auditor-frag-b3-dup` / `FRAG_B3.md` / `out_E3.md` / 16 条

## 三、验收（4 个 task 全做完后，主控侧跑）

```bash
python tools/check.py                          # 8 项结构检查（应全绿；golden --check 已修）
python tools/audit_prep.py diff-dup --pair B:E # frag 双跑漂移（B1-3 vs E1-3）
```

`out_B3P.md` 不被 `audit-count` 认（文件名 B3P 非纯数字结尾），单独检查：

```bash
python - <<'PY'
import re, hashlib, sys
sys.stdout.reconfigure(encoding='utf-8')
p='litrev/_probe/audit/out_B3P.md'
t=open(p,encoding='utf-8').read()
print('戳行:', re.search(r'^> 快照 sha1: (\w+)', t, re.M).group(1), '（应 e894bb155c）')
print('判定行:', len(re.findall(r'^\| B3-10 \|', t, re.M)), '（应 1）')
print('合计行:', re.search(r'^合计：.+$', t, re.M).group(0))
PY
```

预期：`check.py` 退 0；`diff-dup --pair B:E` 输出 frag 三批漂移率；`out_B3P.md` 戳 `e894bb155c`、1 行、有合计行。

## 四、禁止事项

- **不改任何已有判定输出**：`out_B1..B3`、`out_R1..R5`、`out_D1..D5`、`out_S1` 一个字都不动。
- **不补戳**：`out_B3P`/`out_E*` 的戳必须由 auditor 从输入文件原样抄；手工补戳视同伪造证据。
- **不读对照表**：`out_B3P` 的 auditor 不读 `out_B3.md`、`out_S1.md`（含 B3-10 的历史判定）；`out_E*` 的 auditor 不读 `out_B1..B3.md`。
- **不开并发**：4 个 task 顺序执行，避免资源竞争污染一致性测量。
- **不改契约**：本轮固定 v1.1，口径统一（升 v1.2）是后续独立一轮。

## 五、做完回报

回报格式（4 行）：
```
1. auditor-frag-b3-probe → out_B3P.md：1 条（...）；权限拒绝 N 次
2. auditor-frag-b1-dup  → out_E1.md：16 条（...）；权限拒绝 N 次
3. auditor-frag-b2-dup  → out_E2.md：16 条（...）；权限拒绝 N 次
4. auditor-frag-b3-dup  → out_E3.md：16 条（...）；权限拒绝 N 次
```
外加 `check.py` 与 `diff-dup --pair B:E` 的原始输出。**不要自己裁决 B3-10 判得对不对**，交主控验收。
