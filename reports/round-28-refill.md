# round-28：补抽第一批（S2 / C2）与工具改造（2026-11-11）

> 生产就绪四步的第 ③ 步。用户选「判例集优先」：补自足轴判例集 + 抽检自洽，金标准本轮不补。
> 关键前提在动工后被推翻一次（见 §一），C2 因此从 25 条降到 14 条，且换掉了全部选取口径。

## 一、先纠一个读数：「DEP 阳性只确认 3 条」是误记

我最初据以设计 C2 的是「表内 13 条 `DEPENDENT` 阳性只确认了 3 条」。按当前判定表重算三份参考集的人判结果后，事实是：

| 项 | 值 |
|---|---|
| 表内 `DEPENDENT` | 13 |
| 已被金标准人判确认 | 3（`B1-12`、`B3-13`、`R5-06`） |
| 已被判例集 C1 有效样本确认 | 8（`B1-16`、`B2-11`、`B3-09`、`R2-02`、`R2-17`、`R3-08`、`R3-12`、`R4-13`） |
| **三份合并已确认** | **11 / 13** |
| 从未被人判过 | **2**：`B1-09`、`B2-10` |

「3」是**金标准单份**的 DEP 数，不是合并值；C1 里人判 DEPENDENT 的还有 `B1-08`、`B3-08`，但那两条判后被返工，按规矩从分母剔除，不算确认当前文字。

真正的空白因此变成两处：**2 条未确认阳性**，以及 **125 条 SELF 里只有 25 条被人判过（0 差异）、假阴性率完全没测**。C2 据此重新设计，不重复 C1 的「13 条全查」。

## 二、工具改造：参考集可以「另起一批」

原实现把 `SAMPLE_S1` / `GOLDEN` / `CASES_SELF` 写死在模块常量里，`--check` 与 `verify-*` 也读同一组常量，无法新增批次。

改法（`tools/audit_prep.py`）：

- 新增 `apply_batch(kind, name)`：按名字把参考集路径切到 `SAMPLE_<NAME>.md` / `CASES_SELF_<NAME>.md` 等；**默认名 `S1`/`C1` 沿用历史文件名**。
- `pick()` 加 `exclude`（排除上一批 id）与 `k`（直接指定条数）；新增 `read_exclude()`。
- `sample` / `cases` / `verify-sample` / `verify-cases` 四个子命令加 `--name`；`sample` 另加 `--k` / `--exclude`。
- `build_cases` / `build_cases_map` 的标题与文件名引用改为按批次渲染；C1 的说明文字**逐字保留**（它已冻结在人判材料里）。
- `tools/check.py`：11 → **13 项**，新增 `sample --name S2 --check`、`cases --name C2 --check`。

**零回归证据**（改完立刻验）：`check.py` 13/13 绿；三份旧参考集的戳一字未变——S1 `7d1a204d54`、G1 `d46f9e7c3f`、C1 `a4e66877dc`。

## 三、C2：14 条 = 2 未确认阳性 + 12 阴性对照

`CASES_SELF_C2_IDS.txt` 冻结，`CASES_SELF_C2.md` 戳 **`3c036c65ae`**。

| 组 | 口径 | 条数 |
|---|---|---|
| A | 表内 `DEPENDENT` 且未被 G1/C1 人判确认 | **2**（全查：`B1-09`、`B2-10`） |
| B | 表内 `SELF` 且从未进过任何参考集（G1∪C1∪S1） | **12**（`seed=47`，池 85） |

- 排除并集 51 个 id（G1 25 + C1 20 + S1 10 去重），程序化验证 `C2 ∩ (G1∪C1∪S1) = ∅`。
- 工具自检：`cases --name C2 --check` → 14 条（表内 DEP 2），戳 `3c036c65ae`。
- 待填表**不披露**表内判定，也没有组别标注。

## 四、S2：12 条闭卷抽检

`SAMPLE_S2.md` 戳 **`8cf4be2cc9`**，`SAMPLE_S2_KEYS.md` 为答案键（禁止贴给 `auditor-*`）。

- 池 = 排除 S1 已抽 10 条后的 **128** 条 `SUPPORTED`；`seed=71`、`k=12` → 9.4%；`S1 ∩ S2 = ∅`。
- 与 G1/C1 有 4 条重叠（`B1-07`、`B1-16`、`B3-13`、`R3-10`）——**特意保留**：同一批里可以直接比机器与人的判定，是「机器更松」的免费样本。
- 已注册 `BATCHES.json`（`sample_s2 | SAMPLE_S2.md -> out_S2.md`），生成器产出 `auditor-sample-s2`，agent 49 → **50**。
- `out_S2.md` 不进 `audit-count` 默认口径（前缀 `B,R`）。

## 五、两个坑（都实测过，已写进 §五「补抽」）

1. **`--check` 不能吃命令行默认 seed**。首次跑 `sample --name S2 --check` 红：它用默认 `seed=42` 复算 `seed=71` 的批次，头部 `seed=` 对不上。已改为从 `<!-- picks: seed=… -->` 取回生成时点的 `seed`/`rate`。
2. **清单行序会泄露分组**。初版 `CASES_SELF_C2_IDS.txt` 把 A 组排在前面、逐行写「表内 DEPENDENT」，等于把答案递给判定者。已用 `random.Random(47).sample(range(14), 14)` 打散、逐行理由中性化，分组只留答案键。
   —— 附带一个自己的错：第一次打散写成 `sorted(random.Random(47).sample(...))`，对全排列排序等于还原原序，实测顺序没变才发现。

## 六、门禁与状态

```
python tools/check.py  →  ✓ 全部机械自检通过（13 项）
```

判定表未动：`138 条 · S138/P0/U0 · SELF125/DEP13`。

**待办（都是人的活）**：
1. 人开卷填 `CASES_SELF_C2.md` 的 14 行 → `python tools/audit_prep.py verify-cases --name C2`。
2. 重启 OpenCode（`auditor-sample-s2` 生成于本轮）→ 派 `HANDOFF-17.md` 的一行 → `verify-sample --name S2`。

金标准 `G2` 本轮不做，理由写在 RUNBOOK §七 第 10 条：表内 `P0/U0` 时新一批只能抽 `SUPPORTED`，只测过松率；
且人判出的 `PARTIAL` 会立刻变成需要 v1.3 裁决的新分歧，优先级低于自足轴缺口。
