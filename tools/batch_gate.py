#!/usr/bin/env python3
"""生产批次门禁 + 报告生成：`PRODUCTION.md` §三（六门禁）/ §四（抽检）/ §八（四行报告）的机械化版本。

为什么要有这个脚本：六项门禁的读数此前靠人抄、报告靠人手写。人抄的读数无法自证，
漏抄一项也没人发现；而「抽检没做」和「抽检做了但没记」在文字报告里长得一样。
本脚本把「跑门禁 → 读抽检记录 → 判定 → 出报告」串成一条命令，
**门禁红、抽检缺失、抽检条数不够、触发熔断，一律不出报告**。

用法：
  python tools/batch_gate.py --batch rest_b9 --date 2026-11-11
  python tools/batch_gate.py --batch rest_b9 --date 2026-11-11 --note "13 条可直接引用" --write

退出码：0 全过 / 1 门禁红 / 2 抽检记录缺失或不足 / 3 触发熔断
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCHES = ROOT / "litrev/_probe/audit/BATCHES.json"
SAMPLING_DIR = ROOT / "litrev/_probe/audit"
REPORTS = ROOT / "reports"

# PRODUCTION.md §三 的六项门禁 → check.py 里的条目名（前五项）+ 第六项「check.py 整体」
GATES = [
    "verify 全库",
    "card-check 7 节结构",
    "audit-stale --check",
    "batch --check",
    "card-coverage 卡片↔批次对账",
]

# 已知且已定案的永久红项：出现即豁免，**消失也要报**（说明冻结参考集被动了，需重新确认）
EXEMPT = {
    "audit_prep sample S2 --check":
        "冻结参考集因 B2-08 换引文永久失效（RUNBOOK §七 第 16 条），与批次无关",
}


def run(cmd: list[str]) -> tuple[int, str]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def parse_checks(out: str) -> dict[str, bool]:
    """把 check.py 输出解析成 {条目名: 是否通过}。"""
    items: dict[str, bool] = {}
    for line in out.splitlines():
        s = line.strip()
        if not (s.startswith("✓ ") or s.startswith("✗ ")):
            continue
        name = s[2:].split(":")[0].strip()
        # 「回归未通过：<条目>」是 check.py 末尾的汇总行，不是独立条目，
        # 收进来会被当成非豁免红项而误判（红项本身有自己那行）。
        if name.startswith("回归未通过"):
            continue
        items[name] = s.startswith("✓ ")
    return items


def batch_meta(bid: str) -> dict:
    data = json.loads(BATCHES.read_text(encoding="utf-8"))
    for b in data["batches"]:
        if b["id"] == bid:
            return b
    sys.exit(f"[!] BATCHES.json 里没有批次 {bid}")


def parse_out(path: Path) -> list[dict]:
    if not path.exists():
        sys.exit(f"[!] 判定输出不存在：{path}")
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or not re.fullmatch(r"[BR]\d+-\d+", cells[0]):
            continue
        rows.append({"id": cells[0], "supp": cells[1], "self": cells[2]})
    return rows


def prefix_row(out: str, prefix: str) -> dict | None:
    for line in out.splitlines():
        m = re.match(
            rf"^{prefix}\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+✓",
            line.strip())
        if m:
            n, s, p, u, se, de = (int(x) for x in m.groups())
            return {"n": n, "S": s, "P": p, "U": u, "SELF": se, "DEP": de}
    return None


def total_row(out: str) -> dict | None:
    for line in out.splitlines():
        m = re.match(r"^合计\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)",
                     line.strip())
        if m:
            n, s, p, u, se, de = (int(x) for x in m.groups())
            return {"n": n, "S": s, "P": p, "U": u, "SELF": se, "DEP": de}
    return None


def parse_sampling(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or not re.fullmatch(r"[BR]\d+-\d+", cells[0]):
            continue
        rows.append({"id": cells[0], "was": cells[1],
                     "verdict": cells[2], "loose": cells[3]})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True, help="BATCHES.json 里的批次 id，如 rest_b9")
    ap.add_argument("--date", required=True, help="报告日期，如 2026-11-11")
    ap.add_argument("--note", default="", help="§八 第 4 行的处置结论（人写一句）")
    ap.add_argument("--write", action="store_true", help="落盘 reports/batch-<date>-<prefix>.md")
    ap.add_argument("--out", default="", help="指定报告路径（配合 --write）")
    ap.add_argument("--sampling", default="",
                    help="抽检记录路径（默认 litrev/_probe/audit/SAMPLING_<前缀>.md；改它是为了做变异验证）")
    args = ap.parse_args()

    meta = batch_meta(args.batch)
    # 前缀取**输出**文件名（out_R9.md → R9），因为 audit-count 按输出分前缀；
    # 输入文件名是 REST_B9.md，前缀不同（B9），拿它去查会查不到。
    prefix = re.search(r"([BR]\d+)\.md$", meta["output"]).group(1)
    out_path = ROOT / meta["output"]
    rows = parse_out(out_path)

    # ---- 门禁一~五：check.py（含全库 verify / 结构 / 戳 / 覆盖率）----
    rc_chk, out_chk = run([sys.executable, "tools/check.py"])
    items = parse_checks(out_chk)
    gate_fail, gate_lines = [], []
    for g in GATES:
        ok = items.get(g)
        if ok is None:
            gate_fail.append(f"{g}（check.py 里找不到这一项，脚本已与规程脱节）")
        elif not ok:
            gate_fail.append(g)
        gate_lines.append((g, ok))
    # 豁免项：必须仍然是红的；变绿说明冻结参考集被动过，要人工重认
    exempt_state = {k: items.get(k) for k in EXEMPT}
    for k, ok in exempt_state.items():
        if ok is True:
            gate_fail.append(f"{k}（豁免项变绿：冻结参考集可能被改动，需人工重新确认）")
        elif ok is None:
            gate_fail.append(f"{k}（豁免项消失：check.py 的条目已改，需重定豁免清单）")
    # 其余任何非豁免红项都要拦——只查上面五个名字会漏掉金标准/判例集/抽检项
    other_fail = [k for k, v in items.items() if v is False and k not in EXEMPT]
    gate_fail += [f"{k}（非豁免红项）" for k in other_fail]
    overall_ok = not gate_fail
    gate_lines.append(("check.py 整体（非豁免项全绿）", overall_ok))

    # ---- 第六项之外的自校验：audit-count 的分前缀行必须与输出文件一致 ----
    _, out_cnt = run([sys.executable, "litrev/litrev.py", "audit-count"])
    prow, trow = prefix_row(out_cnt, prefix), total_row(out_cnt)
    if prow is None:
        sys.exit(f"[!] audit-count 里没有前缀 {prefix} 的行")
    stat = {
        "n": len(rows),
        "S": sum(1 for r in rows if r["supp"] == "SUPPORTED"),
        "P": sum(1 for r in rows if r["supp"] == "PARTIAL"),
        "U": sum(1 for r in rows if r["supp"] == "UNSUPPORTED"),
        "DEP": sum(1 for r in rows if r["self"] == "DEPENDENT"),
    }
    stat["SELF"] = stat["n"] - stat["DEP"]
    if stat != prow:
        sys.exit(f"[!] 自校验失败：输出文件统计 {stat} ≠ audit-count 行 {prow}"
                 f"（审计员写的合计行与表格行不一致，或输出里有解析不了的行）")

    # ---- §四 抽检记录（人开卷；没有记录就等于没做）----
    sampling = Path(args.sampling) if args.sampling else SAMPLING_DIR / f"SAMPLING_{prefix}.md"
    pool = [r["id"] for r in rows if r["supp"] == "SUPPORTED"]
    need = len(pool) if len(pool) < 10 else math.ceil(len(pool) * 0.20)
    if not sampling.exists():
        print(f"[✗] 抽检记录不存在：{sampling.relative_to(ROOT)}")
        print(f"    本批 SUPPORTED 池 {len(pool)} 条，按 §四 至少抽 {need} 条（{len(pool)<10 and '池<10 全查' or '20%'}）。")
        print("    **没有抽检记录就不出报告**——这是 §四 唯一不能省的人工环节。")
        return 2
    samples = parse_sampling(sampling)
    bad_ids = [s["id"] for s in samples if s["id"] not in pool]
    if bad_ids:
        print(f"[✗] 抽检记录里的 id 不在本批 SUPPORTED 池内：{bad_ids}")
        return 2
    if len(samples) < need:
        print(f"[✗] 抽检条数不足：记了 {len(samples)} 条，§四 要求 ≥{need} 条（池 {len(pool)}）")
        return 2
    loose = [s["id"] for s in samples if s["loose"].strip() == "是"]
    if len(loose) >= 2:
        print(f"[✗] 熔断：一批内偏松 {len(loose)} 条 ≥2（{loose}）→ §五 整批重判，不许只改那两条")
        return 3
    if gate_fail:
        print("[✗] 门禁未全过：")
        for g in gate_fail:
            print("    -", g)
        return 1

    # ---- §八 报告 ----
    L = []
    L.append(f"# 批次报告 · {args.date} · {prefix}（`{args.batch}`）\n")
    L.append(f"1. **本批条数与累计口径**：本批 **{stat['n']} 条**"
             f"（`S{stat['S']}/P{stat['P']}/U{stat['U']}` · `SELF{stat['SELF']}/DEP{stat['DEP']}`）。"
             f"累计 **{trow['n']} 条 · `S{trow['S']}/P{trow['P']}/U{trow['U']}` · "
             f"`SELF{trow['SELF']}/DEP{trow['DEP']}`**。\n")
    L.append("2. **§三 六项门禁**：\n")
    L.append("   | 门禁 | 读数 |")
    L.append("   |---|---|")
    for g, ok in gate_lines[:-1]:
        L.append(f"   | `{g}` | {'✓' if ok else '✗'} |")
    L.append(f"   | `{gate_lines[-1][0]}` | {'✓' if gate_lines[-1][1] else '✗'} |")
    for k, v in EXEMPT.items():
        L.append(f"\n   > 豁免项 `{k}`：{v}")
    L.append("")
    try:
        samp_disp = sampling.relative_to(ROOT).as_posix()
    except ValueError:
        samp_disp = str(sampling)
    L.append(f"3. **§四 抽检**：支撑轴 `SUPPORTED` 池 {len(pool)} 条，"
             f"记录 **{len(samples)} 条（{len(samples)/max(len(pool),1)*100:.1f}%，要求 ≥{need}）**，"
             f"**偏松 {len(loose)} 条**；非 `SUPPORTED` **{stat['P']+stat['U']} 条 100% 过目**。"
             f"**未触发熔断**（阈值：一批内偏松 ≥2 条）。记录见 `{samp_disp}`。\n")
    usable = stat["S"]
    L.append(f"4. **能不能用**：**{usable} 条可直接引用；{stat['P']+stat['U']} 条不可直接用**"
             f"（`PARTIAL`/`UNSUPPORTED`）。"
             + (f" {args.note}" if args.note else "") + "\n")
    text = "\n".join(L)

    print(text)
    if args.write:
        dst = Path(args.out) if args.out else REPORTS / f"batch-{args.date}-{prefix}.md"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text, encoding="utf-8")
        print(f"\n[✓] 已写入 {dst.relative_to(ROOT) if dst.is_absolute() and str(dst).startswith(str(ROOT)) else dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
