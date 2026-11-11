#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""漂移验收标尺（④）：把「两次判定的差异率算大还是算正常」变成一条命令。

背景
  判定表是按固定契约由模型判的。同一批条目再判一次，必然有差异——这是仪器的固有噪声，
  不是错误。问题在于**多大的差异还算噪声**。此前只有基线、没有阈值：

  | 轴 | 基线（131 条配对双跑） | 方向 |
  |---|---|---|
  | 支撑 | 9/131 = 6.9% | 9 : 4（不显著） |
  | 自足 | 12/131 = 9.2% | 11 : 1（单向，P≈0.3%） |
  | 任一 | 25/131 = 19.1% | — |

为什么不直接用「2× 基线」
  实测该规则在不同样本量下**方向相反**：

      n        2× 点估计(自足)     二项 95% 上限(自足)
      12            2.2 条              3 条
      131          24.0 条             18 条

  小样本时它偏严（n=12，2.2 条就报警，而 3 条以内都属正常抽样波动）；
  大样本时它偏松（n=131，24 条才报警，而 18 条就已经超出 95% 区间）。
  样本越小噪声越大，阈值本就该越宽——固定倍率做不到这件事。

本工具的判据
  量级：观测差异数 k 是否超过 Binomial(n, p_hi) 的 95% 分位。
        p_hi 取基线率的 **Wilson 95% 上界**（支撑 0.125 / 自足 0.153 / 任一 0.267），
        而不是点估计——基线本身只有 131 条，点估计有 ±2.5% 的不确定度，
        拿点估计当零假设会把正常波动判成信号。
  方向：自足轴的差异里，`SELF→DEP` 是否占明显多数（≥3:1）。
        基线是 11:1，说明仪器对自足轴**单向偏严**；同向 = 已知偏差，反向 = 口径可能变了。
        （注意：方向判据测的是「是否同向」，不是「是否显著」。n=12 时 3:1 并不显著，
        它只是方向指示，所以方向异常时给「扩样」而不是「信号」。）

用法
  python tools/drift_check.py A.md B.md
  python tools/drift_check.py A.md B.md --json --show 20

退出码
  0 = 噪声（或样本不足，不下结论）   1 = 信号（量级超阈，需逐条查）
  2 = 扩样（方向异常，口径可能变了）  3 = 输入不合法（id 不齐 / 文件无法解析）

只读：本工具不改任何文件，也不参与判定。裁判仍是 `litrev/litrev.py`。
"""

import argparse
import json
import re
import sys
from math import comb, sqrt

# 基线：131 条配对双跑 = REST 83（round-06）+ frag 48（round-07），两组框不重叠。
# 出处 reports/round-07-verification.md §五。合并值是量级参考，不是「131 条同一条件下的双跑」。
BASE = {
    "support": (13, 131),   # 9.9%，方向 P→S 4 : S→P 9（P≈13%，不显著）
    "self": (12, 131),      # 9.2%，方向 SELF→DEP 11 : DEP→SELF 1（P≈0.3%，单向）
    "any": (25, 131),       # 19.1%
}
MIN_N = 10          # 少于这个配对条数，不碰量级判据
DIR_RATIO = 3.0     # 自足轴方向比阈值（基线 11:1）


def wilson_hi(k, n, z=1.96):
    """基线率的 Wilson 95% 上界。基线本身有估计误差，阈值要用上界。"""
    if n == 0:
        return 1.0
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return min(1.0, c + h)


def binom_cdf(k, n, p):
    return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, min(k, n) + 1))


def pct95(n, p):
    """Binomial(n, p) 的 95% 分位：观测差异数 ≤ 它就算量级正常。"""
    for k in range(n + 1):
        if binom_cdf(k, n, p) >= 0.95:
            return k
    return n


def parse_table(text, path):
    """取 (id, 支撑, 自足)。正则与 litrev.parse_audit_rows 同款：只认批次号开头的表格行。"""
    rows, dup = {}, []
    for line in text.splitlines():
        if not re.match(r"^\|\s*[A-Z]+\d+(-\d+)?\s*\|", line):
            continue
        cell = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cell) < 3:
            continue
        rid, sup, slf = cell[0], cell[1], cell[2]
        if not re.fullmatch(r"(SUPPORTED|PARTIAL|UNSUPPORTED)", sup):
            continue
        if not re.fullmatch(r"(SELF|DEPENDENT)", slf):
            continue
        if rid in rows:
            dup.append(rid)
        rows[rid] = (sup, slf)
    if not rows:
        sys.exit(f"[!] {path} 里没有解析出任何判定行")
    if dup:
        sys.exit(f"[!] {path} 里 id 重复：{', '.join(sorted(set(dup))[:5])}")
    return rows


def main():
    ap = argparse.ArgumentParser(add_help=True, description="判定漂移验收标尺")
    ap.add_argument("a", help="第一次判定表（参照）")
    ap.add_argument("b", help="第二次判定表（对照）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--show", type=int, default=8, help="列出前 N 条差异明细（默认 8）")
    args = ap.parse_args()

    A = parse_table(open(args.a, encoding="utf-8", errors="replace").read(), args.a)
    B = parse_table(open(args.b, encoding="utf-8", errors="replace").read(), args.b)

    only_a = sorted(set(A) - set(B))
    only_b = sorted(set(B) - set(A))
    if only_a or only_b:
        print(f"[!] id 集合不一致——两次判定的不是同一批条目，不能算漂移率")
        if only_a:
            print(f"    仅在 A：{len(only_a)} 条  {', '.join(only_a[:6])}{' …' if len(only_a) > 6 else ''}")
        if only_b:
            print(f"    仅在 B：{len(only_b)} 条  {', '.join(only_b[:6])}{' …' if len(only_b) > 6 else ''}")
        sys.exit(3)

    ids = sorted(set(A) & set(B))
    n = len(ids)
    dif_sup, dif_slf, dif_any = [], [], []
    s2d = d2s = 0
    for rid in ids:
        (s1, z1), (s2, z2) = A[rid], B[rid]
        if s1 != s2:
            dif_sup.append((rid, s1, s2))
            dif_any.append(rid)
        if z1 != z2:
            dif_slf.append((rid, z1, z2))
            dif_any.append(rid)
            if z1 == "SELF" and z2 == "DEPENDENT":
                s2d += 1
            elif z1 == "DEPENDENT" and z2 == "SELF":
                d2s += 1

    k = {"support": len(dif_sup), "self": len(dif_slf), "any": len(dif_any)}
    p_hi = {key: wilson_hi(*BASE[key]) for key in BASE}
    thr = {key: pct95(n, p_hi[key]) for key in BASE} if n >= MIN_N else {}

    # ---- 判读 ----
    reasons = []
    if n < MIN_N:
        verdict, code = "样本不足", 0
        reasons.append(f"配对仅 {n} 条（<{MIN_N}），只报数、不下结论；扩到 ≥{MIN_N} 条再判")
    else:
        over = [key for key in ("support", "self", "any") if k[key] > thr[key]]
        if over:
            verdict, code = "信号", 1
            for key in over:
                name = {"support": "支撑", "self": "自足", "any": "任一"}[key]
                reasons.append(
                    f"{name}轴差异 {k[key]}/{n} = {k[key]/n:.1%}，超过 95% 阈值 {thr[key]} 条"
                    f"（H0 率 {p_hi[key]:.3f}）")
        elif k["self"] >= 2 and d2s > s2d:
            verdict, code = "扩样", 2
            reasons.append(
                f"自足轴方向与基线相反：DEP→SELF {d2s} 条 > SELF→DEP {s2d} 条"
                f"（基线 11:1 为单向偏严）——口径可能变了，但 {n} 条不足以裁决")
        else:
            verdict, code = "噪声", 0
            reasons.append(
                f"三轴差异均在 95% 阈值内（支撑 {k['support']}≤{thr['support']}、"
                f"自足 {k['self']}≤{thr['self']}、任一 {k['any']}≤{thr['any']}）")
            if k["self"] == 0:
                reasons.append("自足轴零差异")
            elif s2d and s2d / max(1, s2d + d2s) >= DIR_RATIO / (DIR_RATIO + 1):
                reasons.append(f"自足轴方向与基线同向（SELF→DEP {s2d} : {d2s}，基线 11:1）")
            else:
                reasons.append(
                    f"自足轴方向比 {s2d}:{d2s} 未达 {DIR_RATIO:.0f}:1，"
                    f"但量级在容差内——记录不裁决")

    out = {
        "n": n, "k": k, "rate": {kk: (vk / n if n else 0) for kk, vk in k.items()},
        "threshold": thr, "p_hi": p_hi,
        "direction": {"SELF→DEP": s2d, "DEP→SELF": d2s},
        "verdict": verdict, "code": code, "reasons": reasons,
        "detail": {
            "support": dif_sup[:args.show],
            "self": dif_slf[:args.show],
        },
    }
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        sys.exit(code)

    print(f"配对 {n} 条（{args.a} ↔ {args.b}）")
    print(f"  支撑差异 {k['support']:3d}  {k['support']/n:6.1%}" if n else "")
    print(f"  自足差异 {k['self']:3d}  {k['self']/n:6.1%}   SELF→DEP {s2d} : DEP→SELF {d2s}")
    print(f"  任一差异 {k['any']:3d}  {k['any']/n:6.1%}")
    if thr:
        print(f"  95% 阈值（H0 = 基线 Wilson 上界 {p_hi['support']:.3f}/{p_hi['self']:.3f}/{p_hi['any']:.3f}）")
        print(f"              支撑 {thr['support']} / 自足 {thr['self']} / 任一 {thr['any']} 条")
    print()
    for r in reasons:
        print(f"  · {r}")
    print(f"\n判读：{verdict}")
    if dif_sup or dif_slf:
        print("\n差异明细：")
        for rid, s1, s2 in dif_sup[:args.show]:
            print(f"  {rid}  支撑 {s1} → {s2}")
        for rid, z1, z2 in dif_slf[:args.show]:
            print(f"  {rid}  自足 {z1} → {z2}")
    sys.exit(code)


if __name__ == "__main__":
    main()
