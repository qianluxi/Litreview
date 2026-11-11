# round-31：抽检 S2 回写 —— 11/12，一条支撑差异转 `D-04`

> 输入 `SAMPLE_S2.md`（戳 `8cf4be2cc9`，12 条，闭卷）→ 输出 `out_S2.md`（12 行，戳同源）。
> agent `auditor-sample-s2`（round-28 生成，重启后派发）。**未改判定表、未改卡片、未改任何既有 `out_*.md`。**

## 一、四条验收（全过）

| # | 项 | 结果 |
|---|---|---|
| 1 | 工作区 | `git status` 只多 `out_S2.md`；`SAMPLE_S2.md`、答案键、既有输出均未动 ✓ |
| 2 | 戳与表头 | 首行 `> 快照 sha1: 8cf4be2cc9` ✓；表头与 `out_S1.md` 及契约 §四逐字一致 ✓；12 行 `S01→S12` 同序、合计行齐全 ✓ |
| 3 | 依据逐字 | 引文内连续命中 ≤15 字 12/12 ✓；**主控补核「源 txt 内也命中」12/12**（`norm_text` 归一后比对 12 个源文件，全 OK）✓ |
| 4 | 口径 | `audit-count` 仍 `S138/P0/U0 · SELF125/D13`；`check.py` 13/13 绿 ✓ |

`out_S2.md` 的合计行：`12 条（SUPPORTED 11 / PARTIAL 0 / UNSUPPORTED 1；DEPENDENT 2）`。

## 二、一致率与差异

```
与答案键一致：11/12 · 差异 S04: SUPPORTED→UNSUPPORTED
方向：原表 SUPPORTED → 抽检更严（疑似原表偏松）
```

**11/12 = 91.7%**。注意这个数字只能和漂移基线比，不能当合格证：`verify-sample` 退 1 就是因为这条差异存在，
一致率是描述性的。

唯一差异 `S04`（= `B2-08`，`MaherGomez1996` · 案例或数据的表示形式）已按 §五 登记 `DISPUTED.md` 为 **`D-04`（OPEN）**，
未裁决、未改表。要点：

- 输入逐字相同（论断、引文程序化比对均为 `True`），不存在「换了材料」。
- 判定分歧的实质**不是缺成分，是关系被改写**：引文说「两系统的案例表示**差异**在于属性-值对」，论断说「案例**以**属性-值对**描述**」——`lie in` 的主语是差异，`以…描述` 的主语是案例。属硬规则 9 第 ⑤ 类的关系变体。
- **引文选错了，不是论断写错了**：同篇 p.10 有完整句 `The similarities are the use of attribute-value pairs for representing a case or subcase and the use of models to support CBR.`（`locate` 逐字命中 1.00），直接支撑原论断。换引文即可，论断一字不用改。
- 三方案 α 换引文 / β 改论断 / γ 接受不改，倾向 **α**。预演戳 `FRAG_B2 05632596fd → 1310e0ea75`。

## 三、附带观察（不构成问题，记录备查）

1. **自足轴 2 条 DEP 与原表一致**：`S03`（`easier to avoid overfitting owing to the limited shear wall samples.`，片段无主谓）、
   `S06`（`This selection is the same with the practice engineering.`，`this` + 内容名词回指）都判 `DEPENDENT`，与原表同向。
   但两条的「缺什么」栏都填了 `—`——按填法 `DEPENDENT` 应写明缺哪个指代。**格式瑕疵，不影响判定**，已在下次派发词里提示。
2. **`S09` 与 C2 的 `C01` 是同一节**（`R2-12`，Soibelman p.5 的 Caspian 检索）。两侧都判 `SELF`，是一条跨参考集的一致证据（S2 闭卷机器 vs C2 开卷人）。样本重叠不影响两个集各自的冻结清单。
3. **12 条依据全部是「定位锚点」而非覆盖度证明**（`"0.247"`、`"area ratio"`、`"GraphSAGE"` 这类）。这与 round-22 的结论一致，不要再拿依据栏当「核心成分已覆盖」的证据。

## 四、下一步

1. **裁决 `D-04`**（三方案，倾向 α）。α 需一次重启（`auditor-fix-b6`）+ 一轮 `reseal`。
2. **C2 重填**仍未做（表头已改、答案键 `3c036c65ae`）；与 `D-04` 无依赖，可并行。
3. **④ 漂移标尺**待拍（`round-30` §五 双判方案）。
4. S2 一致率 `11/12` 已可与基线对读，但**样本 12 条定不了点值**，只作方向参考。
