#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""审计层的主控侧准备工具：抽检批次、答案键、人工复核清单、抽检结果验收。

为什么不直接用 `litrev.py sample`：
  那条命令从 `_probe/full/*.md` 的**全部**论断-引文对里抽样，而契约 §七.2 要求的是
  「SUPPORTED 条目按 10%–15% 抽检」。全库抽样会抽到本来就要人看的 PARTIAL/UNSUPPORTED，
  抽检就失去意义。本工具以**当前 8 张判定表**为候选集，只抽 SUPPORTED，并把「抽的是哪条、
  原来判什么」留档在答案键里，供事后机械比对（而不是让审计员自己回忆）。

裁判 `litrev/litrev.py` 一字不改：本工具只读它的输入/输出文件，不参与判定。

用法：
  python tools/audit_prep.py sample                    # 生成 SAMPLE_S1.md + SAMPLE_S1_KEYS.md
  python tools/audit_prep.py sample --check            # 复算并比对现有文件（不改盘）
  python tools/audit_prep.py review                    # 生成 50 条非 SUPPORTED 人工复核清单
  python tools/audit_prep.py verify-sample             # 审计员回写 out_S1.md 后，机械验收
"""

import argparse
import hashlib
import random
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError, OSError):
    pass

ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / "litrev/_probe/audit"
CONTRACT = ROOT / "litrev/_probe/AUDIT_CONTRACT.md"
SAMPLE = AUDIT / "SAMPLE_S1.md"
KEYS = AUDIT / "SAMPLE_S1_KEYS.md"
REVIEW = AUDIT / "REVIEW_NONSUPPORTED.md"
OUT_S1 = AUDIT / "out_S1.md"

IN_NAME = re.compile(r"^FRAG_B(\d+)\.md$|^REST_B(\d+)\.md$")
HEAD = re.compile(r"^###\s+(\S+)\s*・\s*(\S+)\s*・\s*(\S+)\s*・\s*(\S+)\s*$")
ROW_ID = re.compile(r"^\|\s*([A-Z]+\d+-\d+)\s*\|")
STAMP = re.compile(r"^> 快照 sha1: ([0-9a-f]{6,40})", re.M)
CLAIM_LINE = re.compile(r"^- 论断：.+$", re.M)
QUOTE_LINE = re.compile(r"^- 引文：.+$", re.M)
SUPPORT = ("SUPPORTED", "PARTIAL", "UNSUPPORTED")
SELFSUF = ("SELF", "DEPENDENT")


def rel(path):
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def stamp_of(path):
    m = STAMP.search(Path(path).read_text(encoding="utf-8"))
    return m.group(1) if m else None


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse_inputs():
    """批次输入 -> {id: {...}}，论断/引文两行原样保留（audit-stale 已证明它们等于卡片）。"""
    items = {}
    for p in sorted(AUDIT.glob("*.md")):
        if not IN_NAME.match(p.name):
            continue
        text = p.read_text(encoding="utf-8")
        st = stamp_of(p)
        for blk in re.split(r"^### ", text, flags=re.M)[1:]:
            lines = blk.splitlines()
            m = HEAD.match("### " + lines[0].rstrip())
            if not m:
                continue
            i, doc, sec, page = m.groups()
            claim = next((l.rstrip() for l in lines if l.startswith("- 论断：")), "")
            quote_line = next((l.rstrip() for l in lines if l.startswith("- 引文：")), "")
            qm = re.match(r'^- 引文：["\u201c](.+?)["\u201d]\s*(.*)$', quote_line)
            items[i] = {"id": i, "doc": doc, "sec": sec, "page": page,
                        "claim": claim, "quote_line": quote_line,
                        "quote": qm.group(1) if qm else "",
                        "tail": qm.group(2) if qm else "",
                        "batch": p.name, "in_stamp": st}
    return items


def parse_outputs():
    """判定输出 -> {id: {...}}，含支撑/自足/依据/缺什么。"""
    rows = {}
    for p in sorted(AUDIT.glob("out_*.md")):
        if not re.match(r"^out_[BR]\d+\.md$", p.name):
            continue
        text = p.read_text(encoding="utf-8")
        st = stamp_of(p)
        for line in text.splitlines():
            m = ROW_ID.match(line)
            if not m:
                continue
            c = cells(line)
            if len(c) < 5:
                continue
            rows[m.group(1)] = {"support": c[1], "self": c[2],
                                "basis": c[3], "gap": c[4],
                                "out_file": p.name, "out_stamp": st}
    return rows


def load():
    """把输入与判定拼成完整记录，并做三组一致性校验；返回 (records, 各输入戳)。"""
    ins, outs = parse_inputs(), parse_outputs()
    only_in = sorted(set(ins) - set(outs))
    only_out = sorted(set(outs) - set(ins))
    if only_in or only_out:
        sys.exit(f"[!] 批次输入与判定表 id 不齐：只在输入 {only_in} / 只在输出 {only_out}")
    bad = [i for i in ins if ins[i]["in_stamp"] != outs[i]["out_stamp"]]
    if bad:
        sys.exit(f"[!] 这些条目的输入戳与判定戳不一致（判定依据已过期，先跑 audit-stale/batch）：{bad}")
    bad = [i for i in ins if outs[i]["support"] not in SUPPORT or outs[i]["self"] not in SELFSUF]
    if bad:
        sys.exit(f"[!] 判定码非法：{bad}")
    recs = []
    for i in sorted(ins):
        r = dict(ins[i])
        r.update(outs[i])
        recs.append(r)
    stamps = {}
    for r in recs:
        stamps[r["batch"]] = r["in_stamp"]
    return recs, stamps


def pick(recs, rate, seed):
    pool = [r for r in recs if r["support"] == "SUPPORTED"]
    k = max(1, min(len(pool), round(len(pool) * rate)))
    idx = sorted(random.Random(seed).sample(range(len(pool)), k))
    return pool, [pool[j] for j in idx], k


def stamp_text(text):
    """与 litrev.py batch 同算法：只对所有 `- 论断：`/`- 引文：` 行取 sha1 前 10 位。"""
    payload = "".join(re.findall(r"^- (?:论断|引文)：.+$", text, re.M))
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:10]


PICKS_RE = re.compile(r"^<!-- picks: (.*?) -->$", re.M)
ROW_KEY_RE = re.compile(
    r"^\|\s*[SG]\d\d\s*\|\s*([A-Z]+\d+-\d+)\s*\|[^|]*\|[^|]*\|\s*([A-Z]+)\s*\|\s*([A-Z]+)\s*\|"
    r"\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|")


def picks_line(ids, **meta):
    """冻结清单：答案键里记抽样时点的条目 id（可带 pool/k/seed 等元信息）。

    存在理由：抽检与金标准的候选池都是「当前判定表」，判定表一旦被裁决修改，池就移动、
    抽样整体换人，已完成的金标准/抽检会被判成「失效」，逼人重填。冻结清单后，答案键只断言
    「抽样时点抽了哪几条、当时怎么判的」，不再随判定表漂移；判定表改了由 verify-* 报差异。
    """
    parts = [f"{k}={v}" for k, v in meta.items()] + list(ids)
    return "<!-- picks: " + ",".join(parts) + " -->"


def picks_in(path):
    """读回冻结清单 → (ids 或 None, meta)。"""
    if not path.exists():
        return None, {}
    m = PICKS_RE.search(path.read_text(encoding="utf-8"))
    if not m:
        return None, {}
    meta, ids = {}, []
    for tok in m.group(1).split(","):
        tok = tok.strip()
        if not tok:
            continue
        if "=" in tok:
            k, v = tok.split("=", 1)
            meta[k.strip()] = v.strip()
        else:
            ids.append(tok)
    return (ids or None), meta


def recorded_rows(path):
    """从已有答案键的对照表读回「抽样时点原判」：原批次 id → (支撑, 自足, 依据, 缺什么)。"""
    out = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ROW_KEY_RE.match(line)
        if m:
            out[m.group(1)] = (m.group(2), m.group(3), m.group(4), m.group(5))
    return out


def frozen_picks(recs, keys_path, seed):
    """优先用答案键里的冻结清单还原 picked；没有则按当前判定表重抽。"""
    snap, meta = picks_in(keys_path)
    if not snap:
        return None, None, {}
    by_id = {r["id"]: r for r in recs}
    frozen = recorded_rows(keys_path)
    missing = [i for i in snap if i not in by_id]
    if missing:
        sys.exit(f"[!] 冻结清单里的 id 已不在判定表中：{missing}")
    picked = []
    for i in snap:
        r = dict(by_id[i])
        if i in frozen:
            r["support"], r["self"], r["basis"], r["gap"] = frozen[i]
        picked.append(r)
    drift = [i for i in snap
             if i in frozen and (by_id[i]["support"], by_id[i]["self"]) != frozen[i][:2]]
    return picked, meta, {"drift": drift}


def build_sample(recs, picked, pool_n, k, rate, seed, name="S1"):
    # 输入文件必须闭卷：不能出现「这些条目原来都判 SUPPORTED」，否则等于把答案递给审计员。
    # 候选集构成只写在答案键里（主控侧留档，auditor-* 的 read 白名单读不到）。
    head = [
        f"# 抽检批次：{name}",
        "",
        f"> 由 `python tools/audit_prep.py sample` 生成，seed={seed}、rate={rate:.0%}，可复现。",
        f"> 来源 8 个批次、共 {pool_n} 条候选条目，抽 {k} 条（{k/pool_n:.1%}）；"
        "候选集构成由主控留档，不在本文件披露。",
        "> **闭卷**：只给下列五元组，不要回读原文、卡片、其它批次或答案键。",
        "> 快照 sha1: __STAMP__",
        "",
        "## 合计",
        "",
        "| 项 | 数 |",
        "|---|---|",
        f"| 判定表总条目 | {len(recs)} |",
        f"| 候选条目 | {pool_n} |",
        f"| 抽检条目 | {k} |",
        f"| 抽检比例 | {k/pool_n:.1%} |",
        "",
        "## 待判条目",
        "",
    ]
    body = []
    for n, r in enumerate(picked, 1):
        body += [
            f"### S{n:02d} ・ {r['doc']} ・ {r['sec']} ・ {r['page']}",
            "",
            r["claim"],
            r["quote_line"],
            "",
        ]
    raw = "\n".join(head + body).rstrip() + "\n"
    st = stamp_text(raw)
    text = raw.replace("__STAMP__", st, 1)
    return text, st


def build_keys(recs, picked, pool_n, k, rate, seed, stamps, st, name="S1"):
    lines = [
        f"# {name} 答案键（主控侧留档）",
        "",
        f"> 由 `python tools/audit_prep.py sample` 生成，与 `SAMPLE_{name}.md` 同源。",
        f"> 判定表总条目 {len(recs)} · 抽样时点 SUPPORTED {pool_n} · 抽 {k} 条（{k/pool_n:.1%}）· seed={seed} rate={rate:.0%}。",
        f"> 输入快照戳：`{st}`",
        "> **本文件是答案键：禁止贴给任何 `auditor-*`，也不要登记进 `BATCHES.json`。**",
        "> 审计员的 read 白名单只有「契约 + 本批输入」，它读不到本文件；主控也不要在派发提示词里引用它。",
        picks_line([r["id"] for r in picked], pool=pool_n, k=k, seed=seed, rate=f"{rate:g}"),
        "",
        "## 抽样算法（可复现）",
        "",
        f"`pool = [判定表里 support == SUPPORTED 的条目，按 id 升序]`；`k = round({pool_n} * {rate}) = {k}`；"
        f"`idx = sorted(random.Random({seed}).sample(range({pool_n}), {k}))`；取 `pool[idx]`。",
        "",
        "## 源批次输入戳（抽样时的口径）",
        "",
        "| 批次输入 | 快照 sha1 |",
        "|---|---|",
    ]
    for name in sorted(stamps):
        lines.append(f"| `{name}` | `{stamps[name]}` |")
    lines += ["", "## 对照表（抽检 id → 原判定）", "",
              "| 抽检 id | 原批次 id | 文献 | 节 | 原支撑 | 原自足 | 原依据 | 原缺什么 |",
              "|---|---|---|---|---|---|---|---|"]
    for n, r in enumerate(picked, 1):
        lines.append(f"| S{n:02d} | {r['id']} | {r['doc']} | {r['sec']} | "
                     f"{r['support']} | {r['self']} | {r['basis']} | {r['gap']} |")
    lines += ["",
              "> 全部候选条目在抽样时点的支撑码都是 `SUPPORTED`；本文件记录的是**抽样时点的原判**，不是标准答案。",
              "> `verify-sample` 只报差异、不裁定谁对。若报差异，按 RUNBOOK §五：登记争议项、冻结 131 条汇总、",
              "> 先补证据（定向扩抽 / 固定契约双跑），由主控人工裁决后才决定是否整批重审；不自动重审、不逐条修补。",
              "> 上方 `<!-- picks -->` 是**冻结清单**：判定表事后被裁决修改，本文件不失效，`sample --check` 仍按抽样时点原判复现；",
              "> 若要抽新一批，先另存旧文件再重跑 `sample`，不要在旧文件上手改。", ""]
    return "\n".join(lines)


def cmd_sample(args):
    recs, stamps = load()
    picked = meta = drift = None
    if args.check:
        picked, meta, extra = frozen_picks(recs, KEYS, args.seed)
        drift = extra.get("drift", []) if extra else []
    if picked is None:
        pool, picked, k = pick(recs, args.rate, args.seed)
        pool_n = len(pool)
    else:
        pool_n = int((meta or {}).get("pool", len(picked)))
        k = int((meta or {}).get("k", len(picked)))
    text, st = build_sample(recs, picked, pool_n, k, args.rate, args.seed)
    keys = build_keys(recs, picked, pool_n, k, args.rate, args.seed, stamps, st)
    if args.check:
        bad = []
        for path, want in ((SAMPLE, text), (KEYS, keys)):
            if not path.exists():
                bad.append(f"缺失 {path.name}")
            elif path.read_text(encoding="utf-8") != want:
                bad.append(f"与冻结清单复算不一致：{path.name}（输入条目或批次输入变了，需重做抽检）")
        if bad:
            print("✗ 抽检批次自检未通过：")
            for b in bad:
                print("  -", b)
            return 1
        print(f"✓ 抽检批次可复现：{k}/{pool_n} 条（{k/pool_n:.1%}，抽样时点），"
              f"戳 {st}，答案键一致，8 个源批次输入戳未变。")
        if drift:
            print(f"  注：{len(drift)} 条在原判之后被裁决修改（{', '.join(drift)}），"
                  "仍按抽样时点原判复现，差异由 verify-sample 报告。")
        return 0
    SAMPLE.write_text(text, encoding="utf-8")
    KEYS.write_text(keys, encoding="utf-8")
    print(f"判定表 {len(recs)} 条 · SUPPORTED {pool_n} 条 · 抽 {k} 条（{k/pool_n:.1%}，seed={args.seed}）")
    print(f"输入：{rel(SAMPLE)}  > 快照 sha1: {st}")
    print(f"答案键：{rel(KEYS)}（禁止贴给 auditor-*）")
    print("下一步：python tools/gen_subagents.py --check → 在 OpenCode 里派一次 auditor-sample-s1")
    return 0


def cmd_review(args):
    recs, stamps = load()
    bad = [r for r in recs if r["support"] != "SUPPORTED"]
    c = {k: sum(1 for r in bad if r["support"] == k) for k in SUPPORT}
    lines = [
        "# 非 SUPPORTED 人工复核清单",
        "",
        "> 由 `python tools/audit_prep.py review` 从当前 8 张判定表生成；契约 §五.3：任何非 SUPPORTED 必须人看。",
        f"> 共 {len(bad)} 条：PARTIAL {c['PARTIAL']} / UNSUPPORTED {c['UNSUPPORTED']} / 判定表总条目 {len(recs)}。",
        "> 本清单只做待办登记，`复核结论` 与 `处理` 两栏由人填写；判定表一改就重新生成，不要手改条目。",
        "> 引文与论断来自批次输入（已由 `audit-stale` 证明等于卡片当前文字），不要凭记忆改写。",
        "",
        "## 按批次分布",
        "",
        "| 批次输入 | 待复核 |",
        "|---|---|",
    ]
    for name in sorted(stamps):
        lines.append(f"| `{name}` | {sum(1 for r in bad if r['batch'] == name)} |")
    lines += ["", "## 逐条", ""]
    for n, r in enumerate(bad, 1):
        lines += [
            f"### {n:02d} · {r['id']} · {r['doc']} · {r['sec']}",
            "",
            f"- 当前判定：{r['support']} / {r['self']}",
            f"- 引文里的依据：{r['basis']}",
            f"- 缺什么：{r['gap']}",
            r["claim"],
            r["quote_line"],
            "- 复核结论（人填）：",
            "- 处理（人填）：",
            "",
        ]
    REVIEW.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"非 SUPPORTED {len(bad)} 条 → {rel(REVIEW)}"
          f"（PARTIAL {c['PARTIAL']} / UNSUPPORTED {c['UNSUPPORTED']}）")
    return 0


def contract_header():
    for line in CONTRACT.read_text(encoding="utf-8").splitlines():
        if line.startswith("| id | 支撑 | 自足 |"):
            return line
    sys.exit("[!] 契约 §四 里找不到表头，检查 AUDIT_CONTRACT.md")


def cmd_verify_sample(args):
    recs, _ = load()
    if not OUT_S1.exists():
        sys.exit(f"[!] 没有 {OUT_S1.name}，先派 auditor-sample-s1")
    if not KEYS.exists():
        sys.exit("[!] 没有答案键，先跑 sample")
    keys = KEYS.read_text(encoding="utf-8")
    kmap, ksup = {}, {}
    for line in keys.splitlines():
        c = cells(line)
        if len(c) >= 5 and re.match(r"^S\d\d$", c[0]) and re.match(r"^[A-Z]+\d+-\d+$", c[1]):
            kmap[c[0]] = c[1]
            ksup[c[0]] = c[4]
    if not kmap:
        sys.exit("[!] 答案键里没有对照表，先跑 sample")
    st = stamp_of(SAMPLE)
    if not st:
        sys.exit("[!] SAMPLE_S1.md 没有快照戳，先跑 sample")
    out = OUT_S1.read_text(encoding="utf-8")
    olines = out.splitlines()
    first = olines[0] if olines else ""
    if first.strip() != f"> 快照 sha1: {st}":
        # 戳不同源就别往下算「一致率」：样本可能已重抽，拿旧回写比新答案键会得出假数字。
        print(f"✗ 回写与本批输入不同源：")
        print(f"  - {OUT_S1.name} 首行 `{first.strip()}`")
        print(f"  - {SAMPLE.name} 应为 `> 快照 sha1: {st}`")
        print("  → 样本已重抽或回写是旧的，先按当前输入重派一次 auditor-sample-s1，再验收。")
        return 1
    problems, notes = [], []
    notes.append(f"首行戳一致：{st}")

    hdr = contract_header()
    if hdr not in olines:
        problems.append("表头不是契约 §四原文（缺 `| id | 支撑 | 自足 | ... |`）")
    else:
        notes.append("表头与契约 §四逐字一致")

    rows = []
    for line in olines:
        m = re.match(r"^\|\s*(S\d\d)\s*\|", line)
        if not m:
            continue
        c = cells(line)
        rows.append((m.group(1), c))
    ids = [i for i, _ in rows]
    want_ids = [f"S{n:02d}" for n in range(1, len(kmap) + 1)]
    if ids != want_ids:
        problems.append(f"条目数/顺序不对：应为 {want_ids}，实为 {ids}")
    else:
        notes.append(f"判定行 {len(rows)} 条，id 与顺序正确")
    basis_checked = 0
    for i, c in rows:
        if len(c) < 5 or c[1] not in SUPPORT or c[2] not in SELFSUF:
            problems.append(f"{i} 判定码非法：{c[1:3] if len(c) > 2 else c}")
            continue
        src = next((r for r in recs if r["id"] == kmap.get(i)), None)
        if src:
            basis_checked += 1
            basis = c[3].strip().strip('"“”')
            if basis and basis not in src["quote"]:
                problems.append(f"{i} 的「依据」{c[3]} 不在引文里逐字出现")
    if basis_checked:
        notes.append(f"依据逐字命中检查：{basis_checked} 条已比对引文原文")

    mm = re.search(r"合计：(\d+)\s*条.*?SUPPORTED\s*(\d+)\s*/\s*PARTIAL\s*(\d+)\s*/"
                   r"\s*UNSUPPORTED\s*(\d+).*?DEPENDENT\s*(\d+)", out)
    if not mm:
        problems.append("缺合计行或格式不对")
    else:
        want = tuple(int(x) for x in mm.groups())
        got = (len(rows),
               sum(1 for _, c in rows if len(c) > 1 and c[1] == "SUPPORTED"),
               sum(1 for _, c in rows if len(c) > 1 and c[1] == "PARTIAL"),
               sum(1 for _, c in rows if len(c) > 1 and c[1] == "UNSUPPORTED"),
               sum(1 for _, c in rows if len(c) > 2 and c[2] == "DEPENDENT"))
        if want != got:
            problems.append(f"合计行 {want} ≠ 明细 {got}")
        else:
            notes.append(f"合计行自洽：{want}")

    diff = [(i, c[1], ksup.get(i, "?")) for i, c in rows
            if len(c) > 1 and i in ksup and c[1] != ksup[i]]
    # 方向必须分开报：两种差异要重审的对象完全不同。
    strict = [d for d in diff if d[2] == "SUPPORTED" and d[1] != "SUPPORTED"]  # 原表偏松
    loose = [d for d in diff if d[2] != "SUPPORTED" and d[1] == "SUPPORTED"]   # 抽检偏松
    other = [d for d in diff if d not in strict and d not in loose]
    kept = len(rows) - len(diff)
    print(f"抽检回写：{rel(OUT_S1)} · 戳 {st} · {len(rows)} 条")
    for n in notes:
        print("  ✓", n)
    print(f"  与答案键一致：{kept}/{len(rows)}（答案键记录的是抽样时点的原判，不是标准答案）"
          + (f" · 差异 {', '.join(i + ':' + old + '→' + new for i, new, old in diff)}" if diff else ""))
    if diff:
        print("  [i] 机械工具只报差异，不裁定哪一侧判对；格式项与一致项是两套独立判据。")
    if strict:
        print("  [!] 方向：原表 SUPPORTED → 抽检更严（疑似原表偏松）。按 RUNBOOK §五：")
        print("      登记争议项、冻结 131 条汇总，先补证据（定向扩抽 / 固定契约双跑），")
        print("      由主控人工裁决后才决定是否整批重审；不自动整批重审，也不逐条改判定表凑数。")
    if loose:
        print("  [!] 方向：原表非 SUPPORTED → 抽检 SUPPORTED（疑似抽检偏松）。按 RUNBOOK §五：")
        print("      重审对象是抽检侧判读，不是原批次；同样先登记争议项，不自动改任何表。")
    if other:
        print("  [!] 存在双向/跨码差异，逐条列出并交人工裁定。")
    if problems:
        print("\n✗ 未通过：")
        for p in problems:
            print("  -", p)
        return 1
    if diff:
        return 1
    print("\n✓ 抽检格式与命中率全部通过。")
    return 0


GOLDEN = AUDIT / "GOLDEN.md"
GOLDEN_MAP = AUDIT / "GOLDEN_MAP.md"
GOLDEN_QUOTAS = {"SUPPORTED": 15, "PARTIAL": 9, "UNSUPPORTED": 1}


def pick_golden(recs, seed=43):
    """分层抽样：S 15 / P 9 / U 1（U 不足则全抽），seed 固定可复现。"""
    rng = random.Random(seed)
    picked = []
    for s in SUPPORT:
        pool = sorted([r for r in recs if r["support"] == s], key=lambda r: r["id"])
        q = min(GOLDEN_QUOTAS[s], len(pool))
        idx = sorted(rng.sample(range(len(pool)), q))
        picked.extend(pool[j] for j in idx)
    picked.sort(key=lambda r: r["id"])
    return picked


def build_golden(recs, picked):
    head = [
        "# 人工金标准 G1（25 条，开卷裁定）",
        "",
        "> 由 `python tools/audit_prep.py golden` 生成，seed=43，分层（SUPPORTED 15 / PARTIAL 9 / UNSUPPORTED 1）。",
        "> **这是给人填的表，不是给子代理的**：不进 `BATCHES.json`、不生成 agent、`auditor-*` 的 read 白名单不含本文件。",
        "> 判定者可读卡片原文（开卷），独立于判定表给出判定——这是项目唯一的「判得对」参照系。",
        "> 填法：在下表每行填 支撑/自足/依据/缺什么，照契约 §四 表头与判定码；首行原样抄本文件的 `> 快照 sha1:`。",
        "> 不要读 `out_*.md`、`SAMPLE_S1_KEYS.md`、`GOLDEN_MAP.md`；可以读 `litrev/_probe/full/*.md` 卡片原文。",
        "> 快照 sha1: __STAMP__",
        "",
        "## 待填判定表（照契约 §四，人填）",
        "",
        "| id | 支撑 | 自足 | 引文里的依据（≤15 字，必须是引文原词） | 缺什么 / 需补的一句 |",
        "|----|------|------|--------------------------------------|--------------------|",
    ]
    for n, _ in enumerate(picked, 1):
        head.append(f"| G{n:02d} |  |  |  |  |")
    head += ["", "## 条目详情（判定时可读卡片原文，开卷）", ""]
    for n, r in enumerate(picked, 1):
        card = f"litrev/_probe/full/{r['doc']}.md"
        head += [
            f"### G{n:02d} ・ {r['doc']} ・ {r['sec']} ・ {r['page']}",
            "",
            r["claim"],
            r["quote_line"],
            f"- 卡片：`{card}`（可读原文上下文）",
            "",
        ]
    raw = "\n".join(head).rstrip() + "\n"
    st = stamp_text(raw)
    text = raw.replace("__STAMP__", st, 1)
    return text, st


def build_golden_map(recs, picked, st):
    lines = [
        "# G1 金标准映射（主控侧留档，不贴给任何人）",
        "",
        "> 由 `python tools/audit_prep.py golden` 生成，与 `GOLDEN.md` 同源。",
        f"> 判定表总条目 {len(recs)} · 分层抽 {len(picked)} 条 · seed=43。",
        f"> 输入快照戳：`{st}`",
        "> **本文件是答案键**：记录每条 G id 对应的原批次 id 与原判定。判定者填 `GOLDEN.md` 时读不到本文件。",
        "> 人填完后跑 `python tools/audit_prep.py verify-golden` 比对，输出一致率与方向分布。",
        "> 下方 `<!-- picks -->` 是冻结清单：判定表事后被裁决修改，本文件不失效，`golden --check` 仍按抽样时点复现。",
        "",
        picks_line([r["id"] for r in picked]),
        "",
        "## 对照表（G id → 原判定）",
        "",
        "| G id | 原批次 id | 文献 | 节 | 原支撑 | 原自足 | 原依据 | 原缺什么 |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for n, r in enumerate(picked, 1):
        lines.append(f"| G{n:02d} | {r['id']} | {r['doc']} | {r['sec']} | "
                     f"{r['support']} | {r['self']} | {r['basis']} | {r['gap']} |")
    lines += ["", f"> 共 {len(picked)} 条。", ""]
    return "\n".join(lines)


def cmd_golden(args):
    recs, _ = load()
    drift = []
    picked = None
    if args.check:
        picked, _meta, extra = frozen_picks(recs, GOLDEN_MAP, args.seed)
        drift = extra.get("drift", []) if extra else []
    if picked is None:
        picked = pick_golden(recs, args.seed)
    text, st = build_golden(recs, picked)
    gmap = build_golden_map(recs, picked, st)
    n_by = {s: sum(1 for r in picked if r["support"] == s) for s in SUPPORT}
    if args.check:
        bad = []
        # GOLDEN_MAP 全文比对（答案键，无人填，必须与冻结清单逐字一致）
        if not GOLDEN_MAP.exists():
            bad.append("缺失 GOLDEN_MAP.md")
        elif GOLDEN_MAP.read_text(encoding="utf-8") != gmap:
            bad.append("与冻结清单复算不一致：GOLDEN_MAP.md（抽样条目或批次输入变了，需重做金标准）")
        # GOLDEN.md 只比对条目详情部分（表格是人填的，填后必然与空模板不同，不比对）
        marker = "## 条目详情"
        if not GOLDEN.exists():
            bad.append("缺失 GOLDEN.md")
        elif marker not in text:
            bad.append("GOLDEN.md 模板缺少「## 条目详情」标记（工具版本不匹配）")
        else:
            disk = GOLDEN.read_text(encoding="utf-8")
            want_detail = text[text.index(marker):]
            disk_detail = disk[disk.index(marker):] if marker in disk else ""
            if disk_detail != want_detail:
                bad.append("GOLDEN.md 条目详情与当前判定表复算不一致（判定表变了，需重做金标准）")
        if bad:
            print("✗ 金标准自检未通过：")
            for b in bad:
                print("  -", b)
            return 1
        print(f"✓ 金标准可复现：{len(picked)} 条（S{n_by['SUPPORTED']}/P{n_by['PARTIAL']}/U{n_by['UNSUPPORTED']}），戳 {st}。"
              + "（GOLDEN.md 表格为人填部分，不纳入比对）")
        return 0
    GOLDEN.write_text(text, encoding="utf-8")
    GOLDEN_MAP.write_text(gmap, encoding="utf-8")
    print(f"判定表 {len(recs)} 条 · 分层抽 {len(picked)} 条（S{n_by['SUPPORTED']}/P{n_by['PARTIAL']}/U{n_by['UNSUPPORTED']}，seed={args.seed}）")
    print(f"待填表：{rel(GOLDEN)}  > 快照 sha1: {st}")
    print(f"答案键：{rel(GOLDEN_MAP)}（禁止贴给任何人）")
    print("下一步：人填 GOLDEN.md 的判定表 → python tools/audit_prep.py verify-golden")
    return 0


def cmd_verify_golden(args):
    if not GOLDEN.exists() or not GOLDEN_MAP.exists():
        print("✗ 缺 GOLDEN.md 或 GOLDEN_MAP.md（先跑 python tools/audit_prep.py golden）")
        return 1
    gtext = GOLDEN.read_text(encoding="utf-8")
    st = stamp_of(GOLDEN)
    grown = {}
    for line in gtext.splitlines():
        m = re.match(r"^\|\s*(G\d\d)\s*\|", line)
        if not m:
            continue
        c = cells(line)
        if len(c) < 5 or c[1] not in SUPPORT:
            continue
        grown[m.group(1)] = {"support": c[1], "self": c[2], "basis": c[3], "gap": c[4]}
    kmap, krec = {}, {}
    for line in GOLDEN_MAP.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*(G\d\d)\s*\|\s*([A-Z]+\d+-\d+)\s*\|", line)
        if not m:
            continue
        c = cells(line)
        if len(c) < 8:
            continue
        kmap[m.group(1)] = c[1]
        krec[m.group(1)] = {"support": c[4], "self": c[5], "basis": c[6], "gap": c[7]}
    if not kmap:
        print("✗ GOLDEN_MAP.md 解析失败")
        return 1
    want_ids = [f"G{n:02d}" for n in range(1, len(kmap) + 1)]
    filled = [g for g in want_ids if g in grown]
    missing = [g for g in want_ids if g not in grown]
    print(f"金标准回写：{rel(GOLDEN)} · 戳 {st} · 填了 {len(filled)}/{len(kmap)} 条")
    if missing:
        print(f"  [i] 未填：{', '.join(missing)}（填完再复跑）")
    if not filled:
        print("✗ 一条都没填")
        return 1
    sup_same = sum(1 for g in filled if grown[g]["support"] == krec[g]["support"])
    self_same = sum(1 for g in filled if grown[g]["self"] == krec[g]["self"])
    both = sum(1 for g in filled if grown[g]["support"] == krec[g]["support"]
               and grown[g]["self"] == krec[g]["self"])
    strict = [g for g in filled if krec[g]["support"] == "SUPPORTED" and grown[g]["support"] != "SUPPORTED"]
    loose = [g for g in filled if krec[g]["support"] != "SUPPORTED" and grown[g]["support"] == "SUPPORTED"]
    cross = [g for g in filled if grown[g]["support"] != krec[g]["support"] and g not in strict and g not in loose]
    from collections import Counter
    diff_batch = Counter(kmap[g] for g in filled
                         if grown[g]["support"] != krec[g]["support"] or grown[g]["self"] != krec[g]["self"])
    print(f"  支撑轴一致：{sup_same}/{len(filled)}（{sup_same/len(filled):.0%}）")
    print(f"  自足轴一致：{self_same}/{len(filled)}（{self_same/len(filled):.0%}）")
    print(f"  双轴都一致：{both}/{len(filled)}（{both/len(filled):.0%}）")
    if strict:
        print(f"  [!] 人判更严（原 S → 人非 S）{len(strict)} 条：{', '.join(strict)} → 疑似原表偏松")
    if loose:
        print(f"  [!] 人判更松（原非 S → 人 S）{len(loose)} 条：{', '.join(loose)} → 疑似原表偏严")
    if cross:
        print(f"  [!] 跨档差异 {len(cross)} 条：{', '.join(cross)}")
    if diff_batch:
        print(f"  差异按原批次集中：{dict(diff_batch)}")
    print("  [i] 金标准是独立参照系（人开卷裁定），一致率即判定表的可信度估计；")
    print("      差异不自动触发重审，按 RUNBOOK §五 登记 DISPUTED.md 后人工裁决。")
    if missing:
        return 1
    return 0


def cmd_diff_dup(args):
    """比对原判与双跑（默认 out_R* vs out_D*；--pair 可换前缀，如 B:E 比 frag 双跑）。"""
    pair = getattr(args, "pair", "R:D") or "R:D"
    base_pref, _, dup_pref = pair.partition(":")
    base_pref, dup_pref = (base_pref or "R"), (dup_pref or "D")
    rrows, drows = {}, {}
    for p in sorted(AUDIT.glob(f"out_{base_pref}[1-9].md")):
        for line in p.read_text(encoding="utf-8").splitlines():
            m = ROW_ID.match(line)
            if m:
                c = cells(line)
                if len(c) >= 3:
                    rrows[m.group(1)] = (c[1], c[2])
    for p in sorted(AUDIT.glob(f"out_{dup_pref}[1-9].md")):
        for line in p.read_text(encoding="utf-8").splitlines():
            m = ROW_ID.match(line)
            if m:
                c = cells(line)
                if len(c) >= 3:
                    drows[m.group(1)] = (c[1], c[2])
    common = sorted(set(rrows) & set(drows))
    if not common:
        print(f"✗ 没有可配对的 id（out_{base_pref}* 与 out_{dup_pref}* 任一为空，双跑还没跑）")
        return 1
    sup_diff = [(i, rrows[i][0], drows[i][0]) for i in common if rrows[i][0] != drows[i][0]]
    self_diff = [(i, rrows[i][1], drows[i][1]) for i in common if rrows[i][1] != drows[i][1]]
    any_diff = [i for i in common if rrows[i] != drows[i]]
    print(f"双跑配对：{len(common)} 条（{base_pref}* 原判 vs {dup_pref}* 重判）")
    print(f"  支撑轴漂移：{len(sup_diff)}/{len(common)}（{len(sup_diff)/len(common):.1%}）")
    print(f"  自足轴漂移：{len(self_diff)}/{len(common)}（{len(self_diff)/len(common):.1%}）")
    print(f"  任一轴漂移：{len(any_diff)}/{len(common)}（{len(any_diff)/len(common):.1%}）")
    if sup_diff:
        print("  支撑轴差异：")
        for i, r, d in sup_diff:
            print(f"    {i}: {r} → {d}")
    if self_diff:
        print("  自足轴差异：")
        for i, r, d in self_diff:
            print(f"    {i}: {r} → {d}")
    print("  [i] 双跑测的是同输入重复判定的随机漂移，不裁定谁判对；")
    print("      漂移率给「抽检 1/10 差异是噪声还是信号」一个基线（round-04 上界 14.3%）。")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("sample", help="生成 SUPPORTED 抽检批次 + 答案键")
    p.add_argument("--rate", type=float, default=0.12)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--check", action="store_true", help="复算并比对现有文件，不写盘")
    p.set_defaults(func=cmd_sample)
    p = sub.add_parser("review", help="生成非 SUPPORTED 人工复核清单")
    p.set_defaults(func=cmd_review)
    p = sub.add_parser("verify-sample", help="审计员回写 out_S1.md 后机械验收")
    p.set_defaults(func=cmd_verify_sample)
    p = sub.add_parser("golden", help="生成人工金标准 GOLDEN.md + 答案键 GOLDEN_MAP.md")
    p.add_argument("--seed", type=int, default=43)
    p.add_argument("--check", action="store_true", help="复算并比对现有文件，不写盘")
    p.set_defaults(func=cmd_golden)
    p = sub.add_parser("verify-golden", help="人填完 GOLDEN.md 后比对判定表，输出一致率")
    p.set_defaults(func=cmd_verify_golden)
    p = sub.add_parser("diff-dup", help="双跑后比对原判与双跑输出，输出漂移率（默认 R:D）")
    p.add_argument("--pair", default="R:D", help="原判前缀:双跑前缀，默认 R:D；frag 双跑用 B:E")
    p.set_defaults(func=cmd_diff_dup)
    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
