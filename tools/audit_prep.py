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
    # stderr 也必须改：所有停工守卫都走 sys.exit(中文)，它写的是 stderr。
    # 只改 stdout 时，守卫消息会按 Windows 本地码页（cp936）输出，而上层 check.py
    # 用 utf-8 解码 → 读取线程 UnicodeDecodeError，真正的原因被吞掉，只剩 rc=1。
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError, OSError):
    pass

ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / "litrev/_probe/audit"
CONTRACT = ROOT / "litrev/_probe/AUDIT_CONTRACT.md"
SAMPLE = AUDIT / "SAMPLE_S1.md"
KEYS = AUDIT / "SAMPLE_S1_KEYS.md"
REVIEW = AUDIT / "REVIEW_NONSUPPORTED.md"
OUT_S1 = AUDIT / "out_S1.md"

# ---- 参考集批次切换（2026-11-11 加入）----
# 理由：参考集分母见底后要「新增一批」，而项目规则禁止重抽已冻结的清单，
# 所以只能另起文件。默认名（S1/C1）沿用历史文件名 ⇒ 不带 --name 时行为与之前逐字相同。
BATCH_NAME = "S1"
CASE_TAG = "C1"


def apply_batch(kind, name):
    """把参考集路径切到指定批次。只在 cmd_* 入口调用一次。"""
    global SAMPLE, KEYS, OUT_S1, CASE_TAG, CASES, CASES_MAP, CASES_IDS, BATCH_NAME
    if not name:
        return
    n = name.strip().upper()
    BATCH_NAME = n
    if kind == "sample":
        if n != "S1":
            SAMPLE = AUDIT / f"SAMPLE_{n}.md"
            KEYS = AUDIT / f"SAMPLE_{n}_KEYS.md"
            OUT_S1 = AUDIT / f"out_{n}.md"
    elif kind == "cases":
        CASE_TAG = n
        if n != "C1":
            CASES = AUDIT / f"CASES_SELF_{n}.md"
            CASES_MAP = AUDIT / f"CASES_SELF_{n}_KEYS.md"
            CASES_IDS = AUDIT / f"CASES_SELF_{n}_IDS.txt"


def read_exclude(spec):
    """`--exclude a.md,b.md`：从既有参考集读 id，补抽不与上一批重叠（可加性）。"""
    ids = set()
    for part in (spec or "").split(","):
        part = part.strip()
        if not part:
            continue
        p = Path(part) if Path(part).is_absolute() else AUDIT / part
        if not p.exists():
            sys.exit(f"[!] --exclude 指定的文件不存在：{part}")
        snap, _ = picks_in(p)
        if snap:
            ids.update(snap)
        else:
            ids.update(re.findall(r"^###\s+([A-Z]+\d+-\d+)\s*・",
                                  p.read_text(encoding="utf-8"), re.M))
    return ids

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


def pick(recs, rate, seed, exclude=(), k=None):
    """从当前 SUPPORTED 池抽样。

    exclude：补抽时排除上一批已抽中的 id（可加性，不重复消耗同一批条目）。
    k：直接指定条数（补抽更可控），优先于 rate。
    """
    pool = [r for r in recs if r["support"] == "SUPPORTED" and r["id"] not in set(exclude)]
    if k is None:
        k = max(1, min(len(pool), round(len(pool) * rate)))
    else:
        k = max(1, min(len(pool), int(k)))
    idx = sorted(random.Random(seed).sample(range(len(pool)), k))
    return pool, [pool[j] for j in idx], k


def stamp_text(text):
    """与 litrev.py batch 同算法：只对所有 `- 论断：`/`- 引文：` 行取 sha1 前 10 位。"""
    payload = "".join(re.findall(r"^- (?:论断|引文)：.+$", text, re.M))
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:10]


PICKS_RE = re.compile(r"^<!-- picks: (.*?) -->$", re.M)
ROW_KEY_RE = re.compile(
    # 首列是答案键的编号：金标准 G01 / 抽检 S01 / 判例集 C01 —— 一律收，别只认 G、S
    r"^\|\s*[A-Z]\d\d\s*\|\s*([A-Z]+\d+-\d+)\s*\|[^|]*\|[^|]*\|\s*([A-Z]+)\s*\|\s*([A-Z]+)\s*\|"
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


def frozen_total(recs, keys_path):
    """抽样时点的判定表条目数：清单里冻了 total 就用它，否则用当前规模（首次抽样时）。

    存在理由：`build_*` 头部那行「判定表总条目」是抽样时点的展示元信息，不是判定依据。
    判定表后来新增文献（REST_B6 让 131→138）不该让已冻结的抽检/金标准/判例集被判
    「与复算不一致」——那等于逼人重填人开的卷。与 picks 清单同源：元信息也冻结在清单层。
    """
    snap, meta = picks_in(keys_path)
    if snap and "total" in meta:
        return int(meta["total"])
    return len(recs)


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
        f"| 判定表总条目 | {frozen_total(recs, KEYS)} |",
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
    total = frozen_total(recs, KEYS)
    lines = [
        f"# {name} 答案键（主控侧留档）",
        "",
        f"> 由 `python tools/audit_prep.py sample` 生成，与 `SAMPLE_{name}.md` 同源。",
        f"> 判定表总条目 {total} · 抽样时点 SUPPORTED {pool_n} · 抽 {k} 条（{k/pool_n:.1%}）· seed={seed} rate={rate:.0%}。",
        f"> 输入快照戳：`{st}`",
        "> **本文件是答案键：禁止贴给任何 `auditor-*`，也不要登记进 `BATCHES.json`。**",
        "> 审计员的 read 白名单只有「契约 + 本批输入」，它读不到本文件；主控也不要在派发提示词里引用它。",
        picks_line([r["id"] for r in picked], pool=pool_n, k=k, seed=seed,
                   rate=f"{rate:g}", total=total),
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


def key_stamps(path):
    """读答案键里的「源批次输入戳」表 -> {批次文件名: 戳}（抽样时点的历史记录）。"""
    if not Path(path).exists():
        return {}
    out, on = {}, False
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("## 源批次输入戳"):
            on = True
            continue
        if on and line.startswith("## "):
            break
        m = re.match(r"^\|\s*`([^`]+)`\s*\|\s*`([0-9a-f]+)`\s*\|$", line)
        if on and m:
            out[m.group(1)] = m.group(2)
    return out


def cmd_sample(args):
    apply_batch("sample", getattr(args, "name", None))
    recs, stamps = load()
    picked = meta = drift = None
    hist_stamps = {}
    rate = getattr(args, "rate", 0.12)
    seed = getattr(args, "seed", 42)
    if args.check:
        picked, meta, extra = frozen_picks(recs, KEYS, seed)
        drift = extra.get("drift", []) if extra else []
        hist_stamps = key_stamps(KEYS)      # 抽样时点的批次戳，不随后来重封漂移
    if picked is None:
        pool, picked, k = pick(recs, rate, seed,
                               exclude=read_exclude(getattr(args, "exclude", None)),
                               k=getattr(args, "k", None))
        pool_n = len(pool)
        if pool_n:
            rate = k / pool_n               # 用 --k 时回算比例，文件里的说明才与事实一致
    else:
        pool_n = int((meta or {}).get("pool", len(picked)))
        k = int((meta or {}).get("k", len(picked)))
        rate = float((meta or {}).get("rate", rate))   # 自检：按生成时点的比例复现
        seed = int((meta or {}).get("seed", seed))     # 自检：seed 也必须按生成时点复现
    text, st = build_sample(recs, picked, pool_n, k, rate, seed, name=BATCH_NAME)
    keys = build_keys(recs, picked, pool_n, k, rate, seed,
                      hist_stamps or stamps, st, name=BATCH_NAME)
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
        drift_stamp = {n: (hist_stamps.get(n), stamps.get(n)) for n in hist_stamps
                       if stamps.get(n) and stamps.get(n) != hist_stamps[n]}
        print(f"✓ 抽检批次可复现：{k}/{pool_n} 条（{k/pool_n:.1%}，抽样时点），"
              f"戳 {st}，答案键一致"
              + ("。" if not drift_stamp else
                 f"；{len(drift_stamp)} 个批次在抽样后重封（按抽样时点口径复现）："
                 + "、".join(f"{n} {a}→{b}" for n, (a, b) in drift_stamp.items()) + "。"))
        if drift:
            print(f"  注：{len(drift)} 条在原判之后被裁决修改（{', '.join(drift)}），"
                  "仍按抽样时点原判复现，差异由 verify-sample 报告。")
        return 0
    SAMPLE.write_text(text, encoding="utf-8")
    KEYS.write_text(keys, encoding="utf-8")
    print(f"判定表 {len(recs)} 条 · SUPPORTED {pool_n} 条 · 抽 {k} 条（{k/pool_n:.1%}，seed={args.seed}）")
    print(f"输入：{rel(SAMPLE)}  > 快照 sha1: {st}")
    print(f"答案键：{rel(KEYS)}（禁止贴给 auditor-*）")
    print("下一步：python tools/gen_subagents.py --check → 在 OpenCode 里派一次 "
          f"auditor-sample-{BATCH_NAME.lower()}")
    return 0


def cmd_review(args):
    # 防手滑：这份清单由人填写，重生成会抹掉已有结论
    if REVIEW.exists() and not getattr(args, "force", False):
        filled = [l for l in REVIEW.read_text(encoding="utf-8").splitlines()
                  if l.startswith("- 复核结论（人填）") and l.split("：", 1)[-1].strip()]
        if filled:
            sys.exit(f"[!] {rel(REVIEW)} 已有 {len(filled)} 条复核结论，重生成会全部覆盖。"
                     "确认丢弃请加 --force（已填内容可先 git diff 留档）")
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
        "## 填法（只判支撑轴；自足轴已于 v1.2 §八 定案，不要在这里重判）",
        "",
        "每条只填两行，`复核结论` 用**固定词**（便于机械汇总）：",
        "",
        "| 填什么 | 含义 | `处理` 该写什么 |",
        "|---|---|---|",
        "| `维持` | 「缺什么」成立，判定码不改 | 一句话确认缺的是哪个成分（可直接抄缺什么） |",
        "| `改判：SUPPORTED` | 原判偏严，论断每个成分都能在引文里找到 | 指出原「缺什么」误判在哪 |",
        "| `改判：UNSUPPORTED` | 原判偏松，主体/对象与引文不是同一个东西 | 指出换掉了什么 |",
        "| `待定` | 现有材料判不了（要开原文/要补引文） | 写清卡在哪、需要什么 |",
        "",
        "判据只有一条：**论断的每个可检验成分（主体、动作、对象、范围、限定强度）能不能在引文里找到对应表述**；",
        "易错点照契约 §三（情态不得升级、范围不得放大、术语不得替换、否定/缺席需全库证据、论断补主语不算越界）。",
        "开卷：可读 `litrev/_probe/full/` 下对应卡片；不要读 `out_*.md` 之外的他人结论来对答案。",
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


def cmd_verify_review(args):
    """机械汇总 REVIEW_NONSUPPORTED.md 的复核结论：填写率、维持/改判分布、改判缺理由。"""
    if not REVIEW.exists():
        print("✗ 缺 REVIEW_NONSUPPORTED.md（先跑 python tools/audit_prep.py review）")
        return 1
    recs, _ = load()
    live = {r["id"]: r for r in recs}
    items, cid, verdict, note = [], None, "", ""
    for line in REVIEW.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^###\s*\d+\s*·\s*([A-Z]+\d+-\d+)\s*·", line)
        if m:
            if cid:
                items.append((cid, verdict, note))
            cid, verdict, note = m.group(1), "", ""
            continue
        if not cid:
            continue
        if line.startswith("- 复核结论（人填）"):
            verdict = line.split("：", 1)[-1].strip().strip("`").strip()
        elif line.startswith("- 处理（人填）"):
            note = line.split("：", 1)[-1].strip()
    if cid:
        items.append((cid, verdict, note))

    def kind(v):
        if not v:
            return "未填"
        if v.startswith("维持"):
            return "维持"
        if "UNSUPPORTED" in v:
            return "改判 UNSUPPORTED"
        if "SUPPORTED" in v:
            return "改判 SUPPORTED"
        if v.startswith("待定"):
            return "待定"
        return "未识别"

    tally = {}
    changed, no_reason, undone, unknown = [], [], [], []
    for i, v, n in items:
        k = kind(v)
        tally[k] = tally.get(k, 0) + 1
        if k.startswith("改判"):
            changed.append((i, live[i]["support"] if i in live else "?", k.split()[-1], n))
            if not n:
                no_reason.append(i)
        elif k in ("维持",) and not n:
            no_reason.append(i)
        elif k == "待定":
            undone.append(i)
        elif k == "未识别":
            unknown.append((i, v))
    print(f"非 SUPPORTED 复核：{rel(REVIEW)} · 条目 {len(items)} 条")
    order = ["维持", "改判 SUPPORTED", "改判 UNSUPPORTED", "待定", "未识别", "未填"]
    print("  " + "  ".join(f"{k} {tally.get(k, 0)}" for k in order if tally.get(k)))

    # 覆盖门禁：台账只证明「登记过的都填了」，不证明「该登记的都没漏」。
    # 判定表一改（resel / 改稿 / 改判）就可能出现新的非 SUPPORTED，
    # 不重新生成台账时上面那些统计照样全绿 —— 必须与当前判定表对一次。
    in_ledger = {i for i, _, _ in items}
    live_non = [r["id"] for r in recs if r["support"] != "SUPPORTED"]
    unlogged = [i for i in live_non if i not in in_ledger]
    stale = [i for i in in_ledger if i in live and live[i]["support"] == "SUPPORTED"]
    print(f"  覆盖：当前非 SUPPORTED {len(live_non)} 条，台账已登记 {len(live_non) - len(unlogged)} 条")
    if unlogged:
        print(f"  [!] 台账漏登 {len(unlogged)} 条（当前非 SUPPORTED 却不在台账）：{'、'.join(unlogged)}"
              f" → 跑 python tools/audit_prep.py review 重新生成")
    if stale:
        print(f"  [i] 台账另有 {len(stale)} 条已转为 SUPPORTED（历史记录，保留不改）：{'、'.join(stale)}")
    if changed:
        print("  改判明细：")
        for i, old, new, n in changed:
            print(f"    {i}  {old} → {new}" + (f"｜{n[:60]}" if n else "｜（缺处理说明）"))
    if unknown:
        print("  [!] 结论不在词表内：" + "、".join(f"{i}({v})" for i, v in unknown))
    if no_reason:
        print(f"  [!] 有结论但没写「处理」{len(no_reason)} 条：{'、'.join(no_reason)}")
    if undone:
        print(f"  [i] 待定 {len(undone)} 条：{'、'.join(undone)}（需补原文/补引文后回填）")
    left = tally.get("未填", 0)
    if left:
        print(f"  [i] 还有 {left} 条未填")
    bad = bool(unknown or no_reason or undone or left or unlogged)
    print(("✗ 复核未收口" if bad else "✓ 复核已收口：全部有结论、改判均带处理说明"))
    return 1 if bad else 0


def contract_header():
    for line in CONTRACT.read_text(encoding="utf-8").splitlines():
        if line.startswith("| id | 支撑 | 自足 |"):
            return line
    sys.exit("[!] 契约 §四 里找不到表头，检查 AUDIT_CONTRACT.md")


def cmd_verify_sample(args):
    apply_batch("sample", getattr(args, "name", None))
    recs, _ = load()
    if not OUT_S1.exists():
        sys.exit(f"[!] 没有 {OUT_S1.name}，先派 auditor-sample-{BATCH_NAME.lower()}")
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


GOLDEN_ARCHIVE_MARK = "## 原文存档（抽样时点，返工后按此复现）"


def detail_heads(path, prefix):
    """从人填参考集的「条目详情」节抓抽样时点的标题行（含 doc / sec / page）。

    存档节只冻结了论断与引文两行，标题里的页码却跟着当前判定表走。换引文返工时页码会变
    （实测 FIX_B3：金标准 G01 p.13→p.2、判例集 C07 p.23→p.3），`--check` 于是把
    「同一份人判材料」误报成不一致。元信息必须和正文一样按判定时点复现。
    标题行不参与 `stamp_text`（只算 - 论断 / - 引文 行），所以复现它不会动任何戳。
    """
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    marker = "## 条目详情"
    if marker not in text:
        return {}
    out = {}
    for line in text[text.index(marker):].splitlines():
        m = re.match(rf"^### ({prefix}\d\d) ・ .+$", line)
        if m:
            out[m.group(1)] = line
    return out


def golden_archive(recs=None):
    """读金标准的「抽样时点原文」-> {gid: (claim行, 引文行)}。

    为什么要存档：金标准是人对着**抽样时点的论断**判的。稿件返工后论断会变，
    若条目详情跟着当前卡片走，人判就会被悄悄算到新文字上，一致率变成假数字。
    所以详情按存档复现（`golden --check` 仍绿），而 `verify-golden` 用存档 vs 当前
    比对，把「判后被返工」的条目从分母剔除并单列。
    """
    text = GOLDEN_MAP.read_text(encoding="utf-8") if GOLDEN_MAP.exists() else ""
    if GOLDEN_ARCHIVE_MARK in text:
        body = text[text.index(GOLDEN_ARCHIVE_MARK):]
    elif GOLDEN.exists():                      # 首次：从已生成的 GOLDEN.md 详情反推
        body = GOLDEN.read_text(encoding="utf-8")
    else:
        return {}
    arch = {}
    for blk in re.split(r"^### ", body, flags=re.M)[1:]:
        lines = blk.splitlines()
        m = re.match(r"^(G\d\d)\s*・", lines[0])
        if not m:
            continue
        claim = next((l.rstrip() for l in lines if l.startswith("- 论断：")), "")
        quote = next((l.rstrip() for l in lines if l.startswith("- 引文：")), "")
        arch[m.group(1)] = (claim, quote)
    return arch


def build_golden(recs, picked, arch=None, heads=None):
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
        gid = f"G{n:02d}"
        claim, quote = r["claim"], r["quote_line"]
        if arch and gid in arch:               # 判后返工：详情仍按抽样时点复现
            claim, quote = arch[gid]
        card = f"litrev/_probe/full/{r['doc']}.md"
        title = (heads or {}).get(gid) or f"### {gid} ・ {r['doc']} ・ {r['sec']} ・ {r['page']}"
        head += [
            title,
            "",
            claim,
            quote,
            f"- 卡片：`{card}`（可读原文上下文）",
            "",
        ]
    raw = "\n".join(head).rstrip() + "\n"
    st = stamp_text(raw)
    text = raw.replace("__STAMP__", st, 1)
    return text, st


def build_golden_map(recs, picked, st, arch=None):
    total = frozen_total(recs, GOLDEN_MAP)
    lines = [
        "# G1 金标准映射（主控侧留档，不贴给任何人）",
        "",
        "> 由 `python tools/audit_prep.py golden` 生成，与 `GOLDEN.md` 同源。",
        f"> 判定表总条目 {total} · 分层抽 {len(picked)} 条 · seed=43。",
        f"> 输入快照戳：`{st}`",
        "> **本文件是答案键**：记录每条 G id 对应的原批次 id 与原判定。判定者填 `GOLDEN.md` 时读不到本文件。",
        "> 人填完后跑 `python tools/audit_prep.py verify-golden` 比对，输出一致率与方向分布。",
        "> 下方 `<!-- picks -->` 是冻结清单：判定表事后被裁决修改，本文件不失效，`golden --check` 仍按抽样时点复现。",
        "",
        picks_line([r["id"] for r in picked], total=total),
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
    # 原文存档：人判是对着这版文字做的，判后返工不得改写它
    lines += [GOLDEN_ARCHIVE_MARK, "",
              "> 判定时点给出的论断与引文原文。稿件返工后**本节不改写**：`GOLDEN.md` 的条目详情按本节复现，",
              "> `verify-golden` 用本节 vs 当前批次输入比对，把判后被返工的条目列为「失效」并从分母剔除。",
              ""]
    for n, r in enumerate(picked, 1):
        gid = f"G{n:02d}"
        claim, quote = r["claim"], r["quote_line"]
        if arch and gid in arch:
            claim, quote = arch[gid]
        lines += [f"### {gid} ・ {r['id']}", "", claim, quote, ""]
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
    arch = golden_archive() if args.check else None   # 自检按存档复现，重抽用当前原文
    heads = detail_heads(GOLDEN, "G") if args.check else None
    text, st = build_golden(recs, picked, arch, heads)
    gmap = build_golden_map(recs, picked, st, arch)
    n_by = {s: sum(1 for r in picked if r["support"] == s) for s in SUPPORT}
    if args.check:
        bad = []
        # GOLDEN_MAP 全文比对（答案键，无人填，必须与冻结清单逐字一致）
        if not GOLDEN_MAP.exists():
            bad.append("缺失 GOLDEN_MAP.md")
        else:
            disk_map = GOLDEN_MAP.read_text(encoding="utf-8")
            want_map = gmap
            if GOLDEN_ARCHIVE_MARK not in disk_map:
                # 旧版答案键无存档节：只比对存档之前的部分，并提示补写
                want_map = gmap[:gmap.index(GOLDEN_ARCHIVE_MARK)].rstrip() + "\n"
                print("  [i] GOLDEN_MAP 尚无原文存档节（旧版），本次跳过该段比对；"
                      "建议跑一次 `python tools/audit_prep.py golden-migrate` 补写")
            if disk_map != want_map:
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


def cmd_golden_migrate(args):
    """给旧版 GOLDEN_MAP 补写「原文存档」节：存档取自已生成的 GOLDEN.md 条目详情。

    只加存档，不动人物表、不动 picks、不动戳；`--check` 会复算一次确认仍可复现。
    """
    if not GOLDEN.exists() or not GOLDEN_MAP.exists():
        print("✗ 缺 GOLDEN.md 或 GOLDEN_MAP.md")
        return 1
    if GOLDEN_ARCHIVE_MARK in GOLDEN_MAP.read_text(encoding="utf-8"):
        print("[i] GOLDEN_MAP 已有原文存档节，无需迁移")
        return 0
    arch = golden_archive()
    if not arch:
        print("✗ 无法从 GOLDEN.md 反推原文（条目详情为空？）")
        return 1
    recs, _ = load()
    picked, _m, _e = frozen_picks(recs, GOLDEN_MAP, args.seed)
    text, st = build_golden(recs, picked, arch)
    gmap = build_golden_map(recs, picked, st, arch)
    GOLDEN_MAP.write_text(gmap, encoding="utf-8")
    print(f"✓ 已补写原文存档节：{len(arch)} 条（戳 {st}，未改动 GOLDEN.md）")
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

    # 判后返工失效：人判是对着抽样时点的论断做的；稿件改了这条，人判就不能再算进一致率
    arch = golden_archive()
    ins = parse_inputs()
    stale = []
    for g in filled:
        i = kmap.get(g)
        if g in arch and i in ins:
            cur = (ins[i]["claim"], ins[i]["quote_line"])
            if cur != arch[g]:
                stale.append(g)
    active = [g for g in filled if g not in stale]
    if stale:
        print(f"  [!] 判后返工失效 {len(stale)} 条（人判基于旧文，已从分母剔除）："
              f"{', '.join(g + '(' + kmap[g] + ')' for g in stale)}")
    if not active:
        print("✗ 全部分母条目都已失效，需重抽金标准")
        return 1
    filled = active

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


CASES = AUDIT / "CASES_SELF.md"
CASES_MAP = AUDIT / "CASES_SELF_KEYS.md"
CASES_IDS = AUDIT / "CASES_SELF_IDS.txt"


def read_case_ids():
    """从冻结清单读 id（一行 `id | 理由`，`#` 开头为注释）。"""
    if not CASES_IDS.exists():
        sys.exit(f"[!] 缺 {rel(CASES_IDS)}：自足轴判例集的条目清单必须由主控显式冻结")
    ids = []
    for line in CASES_IDS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        i = line.split("|")[0].strip()
        if i:
            ids.append(i)
    if not ids:
        sys.exit(f"[!] {rel(CASES_IDS)} 里没有条目")
    return ids


def build_cases(recs, picked, st_hint=None, arch=None, heads=None):
    head = [
        f"# 自足轴判例集 {CASE_TAG}（{len(picked)} 条，开卷裁定）",
        "",
        f"> 由 `python tools/audit_prep.py cases` 生成；条目清单见 `{CASES_IDS.name}`（冻结，抽完不再重抽）。",
        "> **这是给人填的表**：不进 `BATCHES.json`、不生成 agent、`auditor-*` 的 read 白名单不含本文件。",
        "> 只判**自足轴**，判的对象是**引文这一句本身**（不是论断）：把它单贴出去，读者知不知道在说谁、说什么。",
        "> 契约原话（§二 轴 2 + §五.1）：「引文自带主语与指代，单看这一句就知道在说谁、说什么」；「自足轴只管主语」——",
        "> 只有『主语缺失』或『代词作主语』（`it/this/these/such` + 谓语）才判 `DEPENDENT`；句首的指代性状语不算（主谓齐全 → `SELF`）；",
        "> 片段（名词短语/介词短语/分词，主谓落在引号外）→ `DEPENDENT`；`this paper`/`this section` + 谓语 = 篇章自指 → `SELF`。",
        "> **别拿论断的可读性代替**：片段引文即使论断补得很顺，仍是 `DEPENDENT`；主谓齐全的引文即使论断里有没交代的指称（「前一步」「该系统」），仍是 `SELF`。",
        "> 可读卡片原文（开卷），但不要读 `out_*.md`、",
        f"> `SAMPLE_S1_KEYS.md`、`GOLDEN.md`、`{CASES_MAP.name}`。",
        "> 填法：每行填 自足（`SELF` / `DEPENDENT`）、引文里的依据（≤15 字，必须是引文原词）、",
        "> 缺什么（`DEPENDENT` 必须写明缺的是哪个指代/专有名词；`SELF` 填 `—`）。",
        "> 快照 sha1: __STAMP__",
        "",
        "## 待填判定表（人填）",
        "",
        "| id | 自足 | 引文里的依据（≤15 字，必须是引文原词） | 缺什么 / 需补的一句 |",
        "|----|------|--------------------------------------|--------------------|",
    ]
    for n, _ in enumerate(picked, 1):
        head.append(f"| C{n:02d} |  |  |  |")
    head += ["", "## 条目详情（判定时可读卡片原文，开卷）", ""]
    for n, r in enumerate(picked, 1):
        gid = f"C{n:02d}"
        claim, quote = r["claim"], r["quote_line"]
        if arch and gid in arch:               # 判后返工：详情仍按抽样时点复现
            claim, quote = arch[gid]
        card = f"litrev/_probe/full/{r['doc']}.md"
        title = (heads or {}).get(gid) or f"### {gid} ・ {r['doc']} ・ {r['sec']} ・ {r['page']}"
        head += [
            title,
            "",
            claim,
            quote,
            f"- 卡片：`{card}`（可读原文上下文）",
            "",
        ]
    raw = "\n".join(head).rstrip() + "\n"
    st = stamp_text(raw)
    return raw.replace("__STAMP__", st, 1), st


CASES_ARCHIVE_MARK = "## 原文存档（抽样时点，返工后按此复现）"


def cases_archive():
    """读判例集的「抽样时点原文」-> {cid: (论断行, 引文行)}。

    与金标准同因：人判是对着抽样时点的**论断**做的。稿件返工后论断会变，
    若条目详情跟着当前卡片走，`cases --check` 每轮返工都红，人判却被悄悄算到新文字上。
    → 详情按存档复现；`verify-cases` 用存档 vs 当前比对，把判后被返工的条目从分母剔除。
    """
    if CASES_MAP.exists():
        text = CASES_MAP.read_text(encoding="utf-8")
        if CASES_ARCHIVE_MARK in text:
            body = text[text.index(CASES_ARCHIVE_MARK):]
        elif CASES.exists():                    # 首次：从已生成的 CASES_SELF.md 详情反推
            body = CASES.read_text(encoding="utf-8")
        else:
            return {}
    elif CASES.exists():
        body = CASES.read_text(encoding="utf-8")
    else:
        return {}
    arch = {}
    for blk in re.split(r"^### ", body, flags=re.M)[1:]:
        lines = blk.splitlines()
        m = re.match(r"^(C\d\d)\s*・", lines[0])
        if not m:
            continue
        claim = next((l.rstrip() for l in lines if l.startswith("- 论断：")), "")
        quote = next((l.rstrip() for l in lines if l.startswith("- 引文：")), "")
        arch[m.group(1)] = (claim, quote)
    return arch


def build_cases_map(recs, picked, st, arch=None):
    total = frozen_total(recs, CASES_MAP)
    dep_n = sum(1 for r in picked if r["self"] == "DEPENDENT")
    # C1 的说明文字已冻结在人判材料里，逐字保留；新批次按实际构成写。
    scope = ("表内 DEPENDENT 10 + 双跑边界 10" if CASE_TAG == "C1"
             else f"表内 DEPENDENT {dep_n} + 阴性对照 {len(picked) - dep_n}")
    lines = [
        f"# {CASE_TAG} 自足轴判例集映射（主控侧留档，不贴给任何人）",
        "",
        f"> 由 `python tools/audit_prep.py cases` 生成，与 `{CASES.name}` 同源；条目清单来自 `{CASES_IDS.name}`。",
        f"> 判定表总条目 {total} · 本集 {len(picked)} 条（{scope}）。",
        f"> 输入快照戳：`{st}`",
        "> **本文件是答案键**：记录每条 C id 对应的原批次 id 与表内现判；判定者填表时读不到本文件。",
        "> 人填完后跑 `python tools/audit_prep.py verify-cases`，输出自足轴一致率与方向。",
        "> 下方 `<!-- picks -->` 是冻结清单：判定表事后被裁决修改，本文件不失效，`cases --check` 仍按清单复现。",
        "",
        picks_line([r["id"] for r in picked], total=total),
        "",
        "## 对照表（C id → 表内现判）",
        "",
        "| C id | 原批次 id | 文献 | 节 | 表内支撑 | 表内自足 | 表内依据 | 表内缺什么 |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for n, r in enumerate(picked, 1):
        lines.append(f"| C{n:02d} | {r['id']} | {r['doc']} | {r['sec']} | "
                     f"{r['support']} | {r['self']} | {r['basis']} | {r['gap']} |")
    lines += ["", f"> 共 {len(picked)} 条。", ""]
    # 原文存档：人判是对着这版文字做的，判后返工不得改写它
    lines += [CASES_ARCHIVE_MARK, "",
              "> 判定时点给出的论断与引文原文。稿件返工后**本节不改写**：`CASES_SELF.md` 的条目详情按本节复现，",
              "> `verify-cases` 用本节 vs 当前批次输入比对，把判后被返工的条目列为「失效」并从分母剔除。",
              ""]
    for n, r in enumerate(picked, 1):
        gid = f"C{n:02d}"
        claim, quote = r["claim"], r["quote_line"]
        if arch and gid in arch:
            claim, quote = arch[gid]
        lines += [f"### {gid} ・ {r['id']}", "", claim, quote, ""]
    return "\n".join(lines)



def cmd_cases(args):
    apply_batch("cases", getattr(args, "name", None))
    recs, _ = load()
    by_id = {r["id"]: r for r in recs}
    drift = []
    picked = None
    arch = cases_archive() if args.check else None
    if args.check:
        picked, _meta, extra = frozen_picks(recs, CASES_MAP, None)
        drift = extra.get("drift", []) if extra else []
    if picked is None:
        ids = read_case_ids()
        missing = [i for i in ids if i not in by_id]
        if missing:
            sys.exit(f"[!] 清单里的 id 不在判定表中：{missing}")
        picked = [by_id[i] for i in ids]
    heads = detail_heads(CASES, "C") if args.check else None
    text, st = build_cases(recs, picked, arch=arch, heads=heads)
    cmap = build_cases_map(recs, picked, st, arch=arch)
    if args.check:
        bad = []
        if not CASES_MAP.exists():
            bad.append("缺失 CASES_SELF_KEYS.md")
        elif CASES_MAP.read_text(encoding="utf-8") != cmap:
            bad.append("与冻结清单复算不一致：CASES_SELF_KEYS.md（条目或输入变了，需重做判例集）")
        marker = "## 条目详情"
        if not CASES.exists():
            bad.append("缺失 CASES_SELF.md")
        elif marker not in text:
            bad.append("CASES_SELF.md 模板缺少「## 条目详情」标记（工具版本不匹配）")
        else:
            disk = CASES.read_text(encoding="utf-8")
            disk_detail = disk[disk.index(marker):] if marker in disk else ""
            if disk_detail != text[text.index(marker):]:
                bad.append("CASES_SELF.md 条目详情与当前判定表复算不一致（判定表变了，需重做判例集）")
        if bad:
            print("✗ 自足轴判例集自检未通过：")
            for b in bad:
                print("  -", b)
            return 1
        dep = sum(1 for r in picked if r["self"] == "DEPENDENT")
        print(f"✓ 自足轴判例集可复现：{len(picked)} 条（表内 DEP {dep}），戳 {st}。"
              + "（CASES_SELF.md 表格为人填部分，不纳入比对）")
        if drift:
            print(f"  注：{len(drift)} 条在原判之后被裁决修改（{', '.join(drift)}），仍按清单复现。")
        if arch:
            reworked = [f"{g}({r['id']})" for n, r in enumerate(picked, 1)
                        for g in [f"C{n:02d}"]
                        if g in arch and arch[g] != (r["claim"], r["quote_line"])]
            if reworked:
                print(f"  注：{len(reworked)} 条判后被返工（论断/引文已改），条目详情按存档复现："
                      f"{', '.join(reworked)}")
        return 0
    CASES.write_text(text, encoding="utf-8")
    CASES_MAP.write_text(cmap, encoding="utf-8")
    dep = sum(1 for r in picked if r["self"] == "DEPENDENT")
    print(f"自足轴判例集 {len(picked)} 条（表内 DEPENDENT {dep} / SELF {len(picked)-dep}）")
    print(f"待填表：{rel(CASES)}  > 快照 sha1: {st}")
    print(f"答案键：{rel(CASES_MAP)}（禁止贴给任何人）")
    print(f"下一步：人填 {CASES.name} → python tools/audit_prep.py verify-cases"
          + ("" if CASE_TAG == "C1" else f" --name {CASE_TAG}"))
    return 0


def cmd_cases_migrate(args):
    """给判例集答案键补写「原文存档」节：存档取自 CASES_SELF.md 现存的条目详情。

    为什么需要：判例集原先没有存档，判定表一返工（论断被改写）`cases --check` 就红，
    而人判并不能因此重做。存档补上后详情按抽样时点复现，返工条目由 `verify-cases` 剔除。
    **只改答案键，不动 CASES_SELF.md**（那是人填的，重生成会清空）。
    """
    if not CASES.exists() or not CASES_MAP.exists():
        print("✗ 缺 CASES_SELF.md 或 CASES_SELF_KEYS.md")
        return 1
    if CASES_ARCHIVE_MARK in CASES_MAP.read_text(encoding="utf-8"):
        print("[i] CASES_SELF_KEYS.md 已有原文存档节，无需迁移")
        return 0
    arch = cases_archive()                      # 无存档时自动回落到 CASES_SELF.md 详情
    if not arch:
        print("✗ 无法从 CASES_SELF.md 反推原文（条目详情为空？）")
        return 1
    recs, _ = load()
    picked, _m, _e = frozen_picks(recs, CASES_MAP, None)
    text, st = build_cases(recs, picked, arch=arch)
    cmap = build_cases_map(recs, picked, st, arch=arch)
    marker = "## 条目详情"
    disk = CASES.read_text(encoding="utf-8")
    same = marker in disk and disk[disk.index(marker):] == text[text.index(marker):]
    CASES_MAP.write_text(cmap, encoding="utf-8")
    print(f"✓ 已补写原文存档节：{len(arch)} 条（戳 {st}）")
    print(f"  CASES_SELF.md 未改动；条目详情与存档复现{'一致' if same else '不一致（请跑 cases --check 查明）'}")
    return 0


def cmd_verify_cases(args):
    apply_batch("cases", getattr(args, "name", None))
    if not CASES.exists() or not CASES_MAP.exists():
        print("✗ 缺 CASES_SELF.md 或 CASES_SELF_KEYS.md（先跑 python tools/audit_prep.py cases）")
        return 1
    ctext = CASES.read_text(encoding="utf-8")
    st = stamp_of(CASES)
    filled, blank = {}, []
    for line in ctext.splitlines():
        m = re.match(r"^\|\s*(C\d\d)\s*\|", line)
        if not m:
            continue
        c = cells(line)
        if len(c) < 4:
            continue
        if c[1] not in SELFSUF:
            blank.append(m.group(1))
            continue
        filled[m.group(1)] = {"self": c[1], "basis": c[2], "gap": c[3]}
    kmap, krec = {}, {}
    for line in CASES_MAP.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*(C\d\d)\s*\|\s*([A-Z]+\d+-\d+)\s*\|", line)
        if not m:
            continue
        c = cells(line)
        if len(c) < 8:
            continue
        kmap[m.group(1)] = c[1]
        krec[m.group(1)] = {"support": c[4], "self": c[5]}
    if not kmap:
        print("✗ CASES_SELF_KEYS.md 解析失败")
        return 1
    want = [f"C{n:02d}" for n in range(1, len(kmap) + 1)]
    print(f"自足轴判例集回写：{rel(CASES)} · 戳 {st} · 填了 {len(filled)}/{len(kmap)} 条")
    if blank:
        print(f"  [i] 未填：{', '.join(blank)}")
    if not filled:
        print("✗ 一条都没填")
        return 1
    same = [g for g in want if g in filled and filled[g]["self"] == krec[g]["self"]]
    table_strict = [g for g in want if g in filled
                    and krec[g]["self"] == "DEPENDENT" and filled[g]["self"] == "SELF"]
    table_loose = [g for g in want if g in filled
                   and krec[g]["self"] == "SELF" and filled[g]["self"] == "DEPENDENT"]
    print(f"  自足轴一致：{len(same)}/{len(filled)}（{len(same)/len(filled):.0%}）")
    if table_strict:
        print(f"  [!] 表判 DEPENDENT、回写 SELF {len(table_strict)} 条："
              f"{', '.join(g + '(' + kmap[g] + ')' for g in table_strict)} → 表偏严")
    if table_loose:
        print(f"  [!] 表判 SELF、回写 DEPENDENT {len(table_loose)} 条："
              f"{', '.join(g + '(' + kmap[g] + ')' for g in table_loose)} → 表偏松")
    dep_want = [g for g in want if krec[g]["self"] == "DEPENDENT"]
    dep_ok = [g for g in dep_want if g in filled and filled[g]["self"] == "DEPENDENT"]
    dep_no = [g for g in dep_want if g in filled and filled[g]["self"] != "DEPENDENT"]
    if dep_want:
        print(f"  表内 DEPENDENT 阳性确认：{len(dep_ok)}/{len(dep_want)}"
              + (f"；未确认：{'、'.join(g + '→' + kmap[g] for g in dep_no)}" if dep_no else ""))
    # 冻结基线之后按「当前判定表」再复算一次：改判落表后，上面的数字会永久停在抽样时点，
    # 不给出落地状态就会被误读成「表还没改」。
    recs, _ = load()
    live = {r["id"]: r["self"] for r in recs}
    live_rows = {r["id"]: r for r in recs}
    live_same = [g for g in want if g in filled and kmap[g] in live and filled[g]["self"] == live[kmap[g]]]
    if len(live_same) != len(same):
        tail = "全部与回写一致" if len(live_same) == len(filled) else \
               f"{len(filled) - len(live_same)} 条与回写仍不一致"
        print(f"  按当前判定表复算：{len(live_same)}/{len(filled)}（{tail}；上行为冻结基线，不受改判影响）")
    else:
        print(f"  按当前判定表复算：{len(live_same)}/{len(filled)}（与冻结基线相同，无改判落表）")
    # 判后返工：人是对着抽样时点的论断判的。论断被改过，这条样本就不再是同一条样本，
    # 无论表内自足码有没有跟着变，都不能算进分母（金标准同规矩）。
    arch = cases_archive()
    reworked = [g for g in want if g in arch and kmap.get(g) in live_rows
                and arch[g] != (live_rows[kmap[g]]["claim"], live_rows[kmap[g]]["quote_line"])]
    if reworked:
        eff = [g for g in filled if g not in reworked]
        eff_same = [g for g in eff if filled[g]["self"] == krec[g]["self"]]
        dep_eff = [g for g in eff if krec[g]["self"] == "DEPENDENT"]
        dep_eff_ok = [g for g in dep_eff if filled[g]["self"] == "DEPENDENT"]
        print(f"  [i] 判后返工 {len(reworked)} 条（论断/引文已改，人判不再对应当前文字）："
              f"{'、'.join(g + '(' + kmap[g] + ')' for g in reworked)} → 从分母剔除")
        print(f"      剔除后：自足轴一致 {len(eff_same)}/{len(eff)}"
              f"（{len(eff_same)/len(eff):.0%}）；表内 DEPENDENT 阳性确认 "
              f"{len(dep_eff_ok)}/{len(dep_eff)}")
    print("  [i] 本集只裁自足轴，不裁支撑轴；差异不自动改表，按 RUNBOOK §五 登记 DISPUTED.md 后人工裁决。")
    if blank:
        return 1
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("sample", help="生成 SUPPORTED 抽检批次 + 答案键")
    p.add_argument("--rate", type=float, default=0.12)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--name", help="批次名（默认 S1；补抽用 S2 等，写到 SAMPLE_<NAME>.md）")
    p.add_argument("--k", type=int, help="直接指定抽几条（补抽用，优先于 --rate）")
    p.add_argument("--exclude", help="排除既有答案键里的 id（逗号分隔，保证补抽不重叠）")
    p.add_argument("--check", action="store_true", help="复算并比对现有文件，不写盘")
    p.set_defaults(func=cmd_sample)
    p = sub.add_parser("review", help="生成非 SUPPORTED 人工复核清单")
    p.add_argument("--force", action="store_true", help="已填写时强制重生成（会覆盖复核结论）")
    p.set_defaults(func=cmd_review)
    p = sub.add_parser("verify-review", help="汇总非 SUPPORTED 复核结论（填写率 / 维持 / 改判）")
    p.set_defaults(func=cmd_verify_review)
    p = sub.add_parser("verify-sample", help="审计员回写 out_S1.md 后机械验收")
    p.add_argument("--name", help="批次名（默认 S1）")
    p.set_defaults(func=cmd_verify_sample)
    p = sub.add_parser("golden", help="生成人工金标准 GOLDEN.md + 答案键 GOLDEN_MAP.md")
    p.add_argument("--seed", type=int, default=43)
    p.add_argument("--check", action="store_true", help="复算并比对现有文件，不写盘")
    p.set_defaults(func=cmd_golden)
    p = sub.add_parser("verify-golden", help="人填完 GOLDEN.md 后比对判定表，输出一致率")
    p.set_defaults(func=cmd_verify_golden)
    p = sub.add_parser("golden-migrate", help="给旧版 GOLDEN_MAP 补写原文存档节（不动 GOLDEN.md）")
    p.add_argument("--seed", type=int, default=43)
    p.set_defaults(func=cmd_golden_migrate)
    p = sub.add_parser("diff-dup", help="双跑后比对原判与双跑输出，输出漂移率（默认 R:D）")
    p.add_argument("--pair", default="R:D", help="原判前缀:双跑前缀，默认 R:D；frag 双跑用 B:E")
    p.set_defaults(func=cmd_diff_dup)
    p = sub.add_parser("cases", help="生成自足轴判例集 CASES_SELF.md（人判，条目由 IDS 清单冻结）")
    p.add_argument("--name", help="批次名（默认 C1；补抽用 C2 等，读 CASES_SELF_<NAME>_IDS.txt）")
    p.add_argument("--check", action="store_true", help="复算并比对现有文件，不写盘")
    p.set_defaults(func=cmd_cases)
    p = sub.add_parser("cases-migrate", help="给旧版 CASES_SELF_KEYS.md 补写原文存档节（不动 CASES_SELF.md）")
    p.set_defaults(func=cmd_cases_migrate)
    p = sub.add_parser("verify-cases", help="人填完 CASES_SELF.md 后比对表内现判，输出自足轴一致率")
    p.add_argument("--name", help="批次名（默认 C1）")
    p.set_defaults(func=cmd_verify_cases)
    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
