#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一键回归：跑全部「结构性」机械自检，任一失败退 1。

为什么不含 verify-sample / verify-golden：那两个是「状态相关」的——依赖 out_S1.md 是否回写、
GOLDEN.md 是否填写，没填时一直退 1 会污染回归。它们按需单独跑。本脚本只放「任何时候都该成立」的结构性检查。

用法：python tools/check.py
"""

import pathlib
import re
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError, OSError):
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
PY = sys.executable


def run(cmd):
    # errors="replace"：子进程若有一路输出用了别的编码（例如 sys.exit(中文) 走 stderr），
    # 严格解码会在读取线程抛 UnicodeDecodeError，把「为什么红」连带吞掉。宁可显示乱码也要留下 rc 与正文。
    return subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def verify_all():
    """逐篇 verify，返回 (pass 数, 合计 数, 异常列表)。"""
    files = sorted(p for p in (ROOT / "litrev/_probe/full").glob("*.md") if "引文核验" not in p.name)
    tp = tq = 0
    bad = []
    for p in files:
        r = run([PY, "litrev/litrev.py", "verify", p.as_posix()])
        out = r.stdout or ""
        m = re.search(r"汇总：PASS=(\d+)\s+合计\s*(\d+)", out)
        if not m:
            bad.append(f"{p.name}: 无汇总行 rc={r.returncode}")
            continue
        a, b = map(int, m.groups())
        tp += a
        tq += b
        if a != b or r.returncode != 0:
            bad.append(f"{p.name}: {a}/{b} rc={r.returncode}")
    return tp, tq, bad


CHECKS = [
    ("verify 全库", verify_all),
    ("card-check 7 节结构", [PY, "litrev/litrev.py", "card-check"]),
    ("card-coverage 卡片↔批次对账", [PY, "litrev/litrev.py", "card-coverage"]),
    ("audit-count --check", [PY, "litrev/litrev.py", "audit-count", "--check"]),
    ("audit-count --prefixes S --check", [PY, "litrev/litrev.py", "audit-count", "--prefixes", "S", "--check"]),
    ("audit-stale --check", [PY, "litrev/litrev.py", "audit-stale", "--check"]),
    ("batch --check", [PY, "litrev/litrev.py", "batch", "--check"]),
    ("gen_subagents --check", [PY, "tools/gen_subagents.py", "--check"]),
    ("audit_prep sample --check", [PY, "tools/audit_prep.py", "sample", "--check"]),
    ("audit_prep golden --check", [PY, "tools/audit_prep.py", "golden", "--check"]),
    ("audit_prep cases --check", [PY, "tools/audit_prep.py", "cases", "--check"]),
    ("audit_prep sample S2 --check", [PY, "tools/audit_prep.py", "sample", "--name", "S2", "--check"]),
    ("audit_prep cases C2 --check", [PY, "tools/audit_prep.py", "cases", "--name", "C2", "--check"]),
]


def main():
    fails = []
    for name, spec in CHECKS:
        if callable(spec):
            tp, tq, bad = spec()
            ok = not bad and tp == tq
            if ok:
                print(f"  ✓ {name}: {tp}/{tq} PASS")
            else:
                print(f"  ✗ {name}: {bad[:3]}")
                fails.append(name)
        else:
            r = run(spec)
            lines = [l for l in (r.stdout or "").splitlines() if l.strip()]
            if not lines:  # 停工守卫走 sys.exit(中文) 写的是 stderr，stdout 空
                lines = [l for l in (r.stderr or "").splitlines() if l.strip()]
            tail = lines[-1] if lines else ""
            if len(tail) > 160:  # 守卫常把上百个 id 一行打出来，回归只给摘要
                tail = tail[:160] + f" …（共 {len(tail)} 字符，详情直接跑该命令）"
            if r.returncode == 0:
                print(f"  ✓ {name}: {tail}")
            else:
                print(f"  ✗ {name}: rc={r.returncode} {tail}")
                fails.append(name)
    print()
    if fails:
        print(f"✗ 回归未通过：{', '.join(fails)}")
        return 1
    print("✓ 全部机械自检通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
