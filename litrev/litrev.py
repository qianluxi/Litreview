#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
litrev — 文献综述流水线的可机械验证层

设计原则（对应 loop 的三个必要部件）：
  1) 完成条件可机械判定：引文逐字命中 / 页码正确 / 作者匹配 / 矩阵行数=文献数
  2) 生成与校验分离：本工具只判定，不改写正文
  3) 失败可见：每条给出「标注 vs 实际」，便于回灌给生成方

子命令：
  index    为 PDF 目录建索引（页级文本 + 印张页码偏移 + 重复/扫描件识别 + 文字层健康度）
  text     把 PDF 逐页导出为带页标记的 txt（词级坐标版面重建，修逐词断行）
  locate   给一段（可能是转述的）文字，找回它在原文中的确切句子与页码
  verify   扫描 Markdown 稿，核对每条引文与每条引用标注
  matrix   校验证据矩阵 xlsx：行数、篇目对应、重复、缺失
  sample   按固定比例与种子抽条目，生成可复现的闭卷审计批次
  audit-count  汇总 out_*.md 判定表（唯一允许的汇总口径）并校验各文件合计行

用法示例：
  python litrev.py index
  python litrev.py text --only Borner1993_StructuralSimilarity_CBR
  python litrev.py locate "knowledge available to adapt old solutions"
  python litrev.py verify ../notes/文献综述_初稿_v1.md
  python litrev.py matrix ../notes/证据矩阵_v2_定稿.xlsx
  python litrev.py sample ../_probe/full --rate 0.12 --seed 42 --out ../_probe/audit/SUPPORTED_S1.md
  python litrev.py audit-count --check
"""

import argparse
import csv
import difflib
import gzip
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE = Path(__file__).resolve().parent
PDF_DIR = BASE.parent / "参考文献原文"
IDX_DIR = BASE / "_index"
IDX_FILE = IDX_DIR / "corpus.json.gz"
ALIAS_FILE = BASE / "aliases.json"

LIGATURES = {
    "\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl",
    "\ufb03": "ffi", "\ufb04": "ffl", "\u00ad": "",
}

# ---------------------------------------------------------------- 文本规整


def norm_text(s: str) -> str:
    """把 PDF 抽出的文本规整到「可比较」形态，但保留字符顺序便于回取原文。"""
    for k, v in LIGATURES.items():
        s = s.replace(k, v)
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"-\s*\n\s*", "", s)          # 断词连字符跨行
    s = s.replace("\r", " ")
    s = re.sub(r"[ \t\u00a0]+", " ", s)
    return s.strip()


def key_of(s: str) -> str:
    """检索键：去掉所有空白与标点，只留字母数字与汉字。容忍扫描件字间距损坏。"""
    s = norm_text(s).lower()
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "", s)


def key_with_map(page_text: str):
    """返回 (key, posmap, normalized_text)。posmap[i] 是 key 第 i 个字符在规整文本中的下标。"""
    s = norm_text(page_text)
    chars, pos = [], []
    for i, ch in enumerate(s):
        c = ch.lower()
        if c.isalnum() and (c.isascii() or "\u4e00" <= c <= "\u9fff"):
            chars.append(c)
            pos.append(i)
    return "".join(chars), pos, s


def split_sentences(s: str):
    parts = re.split(r"(?<=[.!?。！？])\s+", s)
    return [p.strip() for p in parts if p and p.strip()]


def fuzzy(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


# ---------------------------------------------------------------- 版面重建
# 有些 PDF 的文字层把每个词、甚至半个词登记成独立「行」（Borner1993 实测 1.03 词/行），
# page.get_text() 于是逐词换行，按行取句只能拿到碎片。这里改用词级坐标重建阅读顺序：
#   1) 以 block 为原子单位，保留段落边界，避免两栏互相穿插
#   2) block 内按 y 聚成视觉行，行内按 x 排序；间距小于阈值不插空格（修 'Similarit' + 'y'）
#   3) block 之间用 XY-cut：先找栏缝竖切，再按 y 间距横切


def _gutter_cut(items, axis, min_gutter):
    """沿 axis（0=x, 1=y）找一条不被任何 item 跨越的缝，切成两侧。"""
    lo, hi = axis, axis + 2
    spans = sorted((i[lo], i[hi]) for i in items)
    merged = []
    for a, b in spans:
        if merged and a <= merged[-1][1] + 1e-6:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    for k in range(len(merged) - 1):
        if merged[k + 1][0] - merged[k][1] >= min_gutter:
            cut = (merged[k][1] + merged[k + 1][0]) / 2
            near = [i for i in items if i[hi] <= cut]
            far = [i for i in items if i[lo] >= cut]
            if near and far and len(near) + len(far) == len(items):
                return near, far
    return None


def _xy_cut(items, min_gutter=8.0, depth=0):
    """items: [(x0, y0, x1, y1, payload)] -> 按阅读顺序重排。"""
    if len(items) <= 1 or depth > 6:
        return sorted(items, key=lambda i: (round(i[1]), i[0]))
    for axis in (0, 1):                      # 先竖切（栏），再横切（段）
        parts = _gutter_cut(items, axis, min_gutter)
        if parts:
            left, right = parts
            return (_xy_cut(left, min_gutter, depth + 1)
                    + _xy_cut(right, min_gutter, depth + 1))
    return sorted(items, key=lambda i: (round(i[1]), i[0]))


def _block_rows(words, ytol=2.5):
    """把一个 block 内的词聚成视觉行 -> [(y中心, [词...]), ...]（行内按 x 排序）。

    按 y 排序后「相邻差分 <= ytol/2」聚成一行，不用 round(y/ytol) 分桶：
    分桶在 66.25pt 这类边界上会把同一条视觉行劈开（中心 66.2 与 66.3 落到不同桶）。
    """
    ws = sorted(words, key=lambda w: (w[1] + w[3]) / 2)
    groups = []
    for w in ws:
        yc = (w[1] + w[3]) / 2
        if groups and abs(yc - groups[-1][0]) <= ytol / 2:
            groups[-1][1].append(w)
            n = len(groups[-1][1])
            groups[-1][0] = (groups[-1][0] * (n - 1) + yc) / n
        else:
            groups.append([yc, [w]])
    return [(yc, sorted(g, key=lambda w: w[0])) for yc, g in groups]


def _join_row(ws, space_gap=1.0):
    """行内按 x 拼词；x 间距小于 space_gap 不插空格（修 'Similarit'+'y'）。"""
    buf, prev_x1 = "", None
    for w in sorted(ws, key=lambda x: x[0]):
        if prev_x1 is not None and w[0] - prev_x1 > space_gap:
            buf += " "
        buf += w[4]
        prev_x1 = w[2]
    return buf.strip()


def _span(ws):
    return min(w[0] for w in ws), max(w[2] for w in ws)


def _same_baseline(a, b, ytol=1.2):
    """两行的 y 中心足够近，且行的纵向范围确实重叠（避免把上/下标当成同一行）。"""
    (ya, wa), (yb, wb) = a, b
    if abs(ya - yb) > ytol:
        return False
    ay0 = min(w[1] for w in wa); ay1 = max(w[3] for w in wa)
    by0 = min(w[1] for w in wb); by1 = max(w[3] for w in wb)
    return min(ay1, by1) - max(ay0, by0) > 0


def _merge_rows(rows):
    """PyMuPDF 会把一条视觉行切成两个 block（标题/正文同基线连排时常见）。
    同基线且 x 区间交叠 → 并回一行；真双栏的 x 区间不交叠，不会被误合。
    合并结果保留「首次出现」的位置，因此不破坏 XY-cut 给出的分栏阅读顺序。"""
    merged = []
    for r in rows:
        for i, m in enumerate(merged):
            if _same_baseline(m, r):
                a0, a1 = _span(m[1])
                b0, b1 = _span(r[1])
                if a0 < b1 and b0 < a1:          # x 区间交叠 = 同一条视觉行被切开
                    ws = m[1] + r[1]
                    merged[i] = (sum((w[1] + w[3]) / 2 for w in ws) / len(ws), ws)
                    break
        else:
            merged.append(r)
    return merged


def _block_lines(words, ytol=2.5, space_gap=1.0):
    """把一个 block 内的词重建为若干视觉行。"""
    return [l for l in (_join_row(ws, space_gap) for _, ws in _block_rows(words, ytol)) if l]


def page_layout_text(page):
    """按版面重建单页正文（词级坐标）。无词时退回 get_text()。"""
    words = page.get_text("words")
    if not words:
        return page.get_text()
    by_block = {}
    for w in words:
        by_block.setdefault(w[5], []).append(w)
    items = [(b[0], b[1], b[2], b[3], by_block[b[5]])
             for b in page.get_text("blocks") if b[5] in by_block]
    if not items:
        return page.get_text()
    rows = []
    for item in _xy_cut(items):
        rows.extend(_block_rows(item[4]))
    return "\n".join(_join_row(ws) for _, ws in _merge_rows(rows))


def text_health(text):
    """文字层健康度：词/行 与 短行占比。词/行 < 3 基本可判定逐词断行。"""
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        return {"lines": 0, "words": 0, "wpl": 0.0, "short": 1.0}
    words = sum(len(l.split()) for l in lines)
    short = sum(1 for l in lines if len(l.split()) <= 3) / len(lines)
    return {"lines": len(lines), "words": words,
            "wpl": round(words / len(lines), 2), "short": round(short, 3)}


# ---------------------------------------------------------------- 文件名与作者

YEAR_RE = re.compile(r"(19|20)\d{2}")


def file_stem_author(fname: str):
    """Borner1993_StructuralSimilarity_CBR.pdf -> ('Borner', 1993)"""
    stem = Path(fname).stem
    m = YEAR_RE.search(stem)
    year = int(m.group(0)) if m else None
    head = stem[: m.start()] if m else stem
    raw = re.sub(r"[^A-Za-z]", "", head)
    return raw, year


def load_aliases():
    if ALIAS_FILE.exists():
        return json.loads(ALIAS_FILE.read_text(encoding="utf-8"))
    return {}


def surnames_for(fname: str, aliases: dict):
    """该文件可被接受的引用姓氏（规整后小写，去空格）。"""
    names = set()
    raw, _ = file_stem_author(fname)
    if raw:
        names.add(raw.lower())
    for k in aliases.get(fname, []):
        names.add(re.sub(r"[^a-z]", "", k.lower()))
    # 已知的多作者组合：从文件名剥离年份后按大写切分不可靠，故补 token 级匹配
    return names


def surname_tokens(alias_str: str):
    toks = re.split(r"[^a-z]+", alias_str.lower())
    return [t for t in toks if len(t) >= 4]


# ---------------------------------------------------------------- 导出正文


def cmd_text(args):
    """把 PDF 逐页导出为带 <<<PAGE n>>> 标记的 txt，供 extractor 读。

    默认用版面重建（词级坐标）而不是 page.get_text()：后者在逐词断行的 PDF 上
    会把一句话拆成几十行，抽取方按行取句只能得到碎片。
    """
    import pymupdf

    pdf_dir = Path(args.dir).resolve()
    out_dir = Path(args.out).resolve() if args.out else (BASE / "_probe" / "texts")
    only = {s.strip() for s in args.only.split(",")} if args.only else None
    files = sorted(pdf_dir.glob("*.pdf"))
    if only:
        files = [f for f in files if f.stem in only]
    if not files:
        print(f"[!] {pdf_dir} 下没有匹配的 PDF")
        return 1

    rows = []
    if not args.dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    for f in files:
        doc = pymupdf.open(f)
        pages, raw_all = [], []
        for i, pg in enumerate(doc):
            raw = pg.get_text()
            lay = page_layout_text(pg) if args.layout else raw
            raw_all.append(raw)
            pages.append(f"<<<PAGE {i + 1}>>>\n{lay.strip()}\n")
        n = len(pages)
        doc.close()

        body = "\n".join(pages)
        before = text_health("\n".join(raw_all))
        after = text_health(body)
        rows.append((f.stem, n, before, after))

        if not args.dry_run:
            header = (f"# SOURCE: {f.name}\n"
                      f"# PDF 物理页数: {n}\n\n")
            (out_dir / (f.stem + ".txt")).write_text(header + body, encoding="utf-8")

    print(f"{'文献':52s} {'页':>3s}  词/行 (raw→layout)   短行占比")
    print("-" * 96)
    bad = []
    for stem, n, b, a in rows:
        mark = "  ← 仍碎片" if a["wpl"] < 3 else ""
        print(f"{stem[:52]:52s} {n:3d}   {b['wpl']:5.2f} → {a['wpl']:5.2f}"
              f"        {b['short']*100:5.1f}% → {a['short']*100:5.1f}%{mark}")
        if a["wpl"] < 3:
            bad.append(stem)

    if args.dry_run:
        print("\n(dry-run：未写入文件)")
    else:
        print(f"\n已写入 {out_dir}")
    if bad:
        print("\n[!] 版面重建后仍低于 3 词/行，这批文字层坏到无法按行取句，必须 OCR 或视觉抄录：")
        for s in bad:
            print(f"  - {s}")
    return 0


# ---------------------------------------------------------------- 建索引


def detect_printed_offset(doc):
    """用页眉/页脚里的孤立数字推断「印张页码 = PDF 页 + offset」。"""
    c = Counter()
    for i, pg in enumerate(doc):
        lines = [l.strip() for l in pg.get_text().split("\n") if l.strip()]
        if not lines:
            continue
        for cand in (lines[0], lines[-1]):
            if re.fullmatch(r"\d{1,4}", cand):
                d = int(cand) - (i + 1)
                if -3 <= d <= 60:
                    c[d] += 1
    if not c:
        return None
    d, n = c.most_common(1)[0]
    return d if n >= max(3, len(doc) // 5) else None


def cmd_index(args):
    import pymupdf

    pdf_dir = Path(args.dir).resolve()
    files = sorted(pdf_dir.glob("*.pdf"))
    if not files:
        print(f"[!] {pdf_dir} 下没有 PDF")
        return 1

    IDX_DIR.mkdir(parents=True, exist_ok=True)
    corpus, manifest, sigs = {}, [], {}

    for f in files:
        try:
            doc = pymupdf.open(f)
        except Exception as e:
            print(f"[!] 无法打开 {f.name}: {e}")
            continue

        pages, keys, lay_texts = [], [], []
        for i, pg in enumerate(doc):
            k = key_of(pg.get_text())
            lay = page_layout_text(pg)
            kb = key_of(lay)
            keys.append(k)
            lay_texts.append(lay)
            rec = {"p": i + 1, "k": k}
            # 版面重建后的键只在它比 raw 键更「完整」时另存一份：
            # 两栏乱序、逐词断行都会让两者不同；正常页两键一致，不占空间
            if kb and kb != k:
                rec["kb"] = kb
            pages.append(rec)

        total_chars = sum(len(k) for k in keys)
        empty = sum(1 for k in keys if len(k) < 50)
        offset = detect_printed_offset(doc)
        health = text_health("\n".join(lay_texts))

        sig = key_of("".join(keys[:2]))[:5000]
        corpus[f.name] = {"pages": pages, "offset": offset, "n": len(pages)}
        sigs[f.name] = sig
        manifest.append({
            "file": f.name,
            "pages": len(pages),
            "chars": total_chars,
            "empty_pages": empty,
            "words_per_line": health["wpl"],
            "short_line_ratio": health["short"],
            "printed_offset": "" if offset is None else offset,
            "scanned": "是" if total_chars < len(pages) * 120 else "",
            "fragmented": "是" if health["wpl"] < 3 else "",
            "duplicate_of": "",
        })
        doc.close()

    # ---- 去重：正文键取中段长切片，若在另一文件的全文键中原样出现，视为同一文献 ----
    # 不依赖页数，可识别「期刊版 / 网页版 / 预印本」这类排版不同但正文相同的情况
    by_name = {m["file"]: m for m in manifest}
    full = {f: "".join(p["k"] for p in corpus[f]["pages"]) for f in corpus}
    used = set()
    names = list(full)
    for i, a in enumerate(names):
        if a in used or len(full[a]) < 2000:
            continue
        members = {a}
        probes = []
        for frac in (0.3, 0.5, 0.7):
            start = int(len(full[a]) * frac)
            probes.append(full[a][start: start + 120])
        for b in names[i + 1:]:
            if b in used or len(full[b]) < 2000:
                continue
            if any(pr and pr in full[b] for pr in probes):
                members.add(b)
        if len(members) > 1:
            keep = sorted(members, key=lambda f: (hit_priority(f), f))[0]
            for m in members:
                if m != keep:
                    by_name[m]["duplicate_of"] = keep
            used |= members

    with gzip.open(IDX_FILE, "wt", encoding="utf-8") as fh:
        json.dump(corpus, fh, ensure_ascii=False)

    with open(IDX_DIR / "manifest.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(manifest[0].keys()))
        w.writeheader()
        w.writerows(manifest)

    uniq = [m for m in manifest if not m["duplicate_of"]]
    scanned = [m for m in manifest if m["scanned"]]
    frag = [m for m in manifest if m["fragmented"]]
    print(f"索引完成：{len(manifest)} 个 PDF，去重后 {len(uniq)} 篇，共 {sum(m['pages'] for m in manifest)} 页")
    print(f"索引文件：{IDX_FILE}  ({IDX_FILE.stat().st_size/1e6:.1f} MB)")
    if scanned:
        print("\n无文字层 / 抽取几乎为空（必须 OCR 或人工核对，不可交给自动校验）：")
        for m in scanned:
            print(f"  - {m['file']}  ({m['pages']} 页，仅 {m['chars']} 字符)")
    if frag:
        print("\n文字层逐词断行（版面重建后仍 < 3 词/行，按行取句必得碎片，先跑 text 子命令核对）：")
        for m in frag:
            print(f"  - {m['file']}  ({m['words_per_line']} 词/行，短行 {m['short_line_ratio']*100:.0f}%)")
    if len(manifest) != len(uniq):
        print("\n内容重复（保留一份即可，矩阵里会出现重复行）：")
        for m in manifest:
            if m["duplicate_of"]:
                print(f"  - {m['file']}  ==  {m['duplicate_of']}")
    print(f"\n明细：{IDX_DIR/'manifest.csv'}")
    return 0


def load_corpus():
    if not IDX_FILE.exists():
        print("[!] 索引不存在，先运行：python litrev.py index")
        sys.exit(2)
    with gzip.open(IDX_FILE, "rt", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------- 定位


def search_exact(corpus, qkey, only=None):
    hits = []
    if len(qkey) < 12:
        return hits
    for fname, rec in corpus.items():
        if only and fname not in only:
            continue
        for pg in rec["pages"]:
            if qkey in pg["k"] or qkey in pg.get("kb", ""):
                hits.append((fname, pg["p"]))
    return hits


def search_fuzzy(corpus, quote, only=None, topk=3):
    """逐字找不到时，用罕见词定位候选页，再在句级做相似度比对。"""
    toks = sorted({t for t in re.findall(r"[a-z]{5,}", quote.lower())}, key=len, reverse=True)[:5]
    if not toks:
        return []
    cands = []
    for fname, rec in corpus.items():
        if only and fname not in only:
            continue
        for pg in rec["pages"]:
            k = pg["k"]
            hit = sum(1 for t in toks if t in k)
            if hit >= max(2, len(toks) // 2):
                # 粗筛后再精算
                seg = k
                score = fuzzy(key_of(quote), seg[: max(len(key_of(quote)) * 2, 400)])
                cands.append((hit, fname, pg["p"]))
    cands.sort(reverse=True)
    return cands[:topk]


def best_sentence_in_page(fname, pno, quote):
    """回到 PDF 取该页原文，找出与 quote 最相似的句子。"""
    import pymupdf
    doc = pymupdf.open(PDF_DIR / fname)
    try:
        if pno < 1 or pno > len(doc):
            return None, 0.0
        raw = doc[pno - 1].get_text()
    finally:
        doc.close()
    qk = key_of(quote)
    best, best_r = None, 0.0
    for s in split_sentences(norm_text(raw)):
        if len(s) < 25:
            continue
        r = fuzzy(qk, key_of(s))
        if r > best_r:
            best, best_r = s, r
    return best, best_r


def find_quote(corpus, quote, only=None):
    """返回 dict(file, page, exact, ratio, sentence)。"""
    qk = key_of(quote)
    hits = search_exact(corpus, qk, only)
    if hits:
        # 多个命中（重复文件）时优先非重复文件
        f, p = hits[0]
        return {"file": f, "page": p, "exact": True, "ratio": 1.0,
                "all_hits": hits, "sentence": quote}
    for _, f, p in search_fuzzy(corpus, quote, only):
        sent, r = best_sentence_in_page(f, p, quote)
        if sent and r >= 0.55:
            return {"file": f, "page": p, "exact": False, "ratio": r,
                    "all_hits": [], "sentence": sent}
    return None


# ---------------------------------------------------------------- 解析 Markdown

Q_ASCII = re.compile(r'"([^"\n]{15,500})"')
Q_CJK = re.compile(r"[“]([^”\n]{15,500})[”]")
PAGE_RE = re.compile(r"\bp{1,2}\.\s*(\d{1,4})")


def guess_author(text, corpus, aliases):
    """在引文之前的窗口里找最近的、库内可识别的姓氏。"""
    names = []
    for fname in corpus:
        for s in surnames_for(fname, aliases):
            if s:
                names.append(s)
                names.extend(surname_tokens(s))
    names = sorted({n for n in names if len(n) >= 4}, key=len, reverse=True)
    low = text.lower()
    best, best_pos = None, -1
    for n in names:
        i = low.rfind(n)
        if i > best_pos:
            best, best_pos = n, i
    return best


def _pairs(text, ch):
    """按出现顺序成对，避免「前一个闭合引号到下一个开引号」的假跨段匹配。"""
    out, i = [], 0
    while True:
        a = text.find(ch, i)
        if a < 0:
            break
        b = text.find(ch, a + 1)
        if b < 0:
            break
        out.append((a, b))
        i = b + 1
    return out


def parse_citations(md):
    spans = []
    for a, b in _pairs(md, '"'):
        spans.append((a, b))
    i = 0
    while True:
        a = md.find("\u201c", i)
        if a < 0:
            break
        b = md.find("\u201d", a + 1)
        if b < 0:
            break
        spans.append((a, b))
        i = b + 1
    spans.sort()

    items = []
    for a, b in spans:
        q = md[a + 1: b].strip()
        if not q or "\n" in q:
            continue
        n_letters = len(re.findall(r"[A-Za-z]", q))
        n_cjk = len(re.findall(r"[\u4e00-\u9fa5]", q))
        if n_letters >= 20 and n_cjk <= 2:
            kind = "EN"
        elif n_cjk >= 25 and n_letters <= 40:
            kind = "ZH"
        else:
            continue
        tail = md[b + 1: b + 141]
        pm = PAGE_RE.search(tail)
        page = int(pm.group(1)) if pm else None
        head = tail[: pm.start()] if pm else ""
        author, ctx_year = None, None
        cleaned = re.sub(r"^[（(\s]+", "", head)
        parts = [x.strip() for x in re.split(r"[,，]", cleaned) if x.strip()]
        for k, p in enumerate(parts):
            if re.fullmatch(r"(19|20)\d{2}", p):
                ctx_year = int(p)
                if k > 0:
                    author = parts[k - 1]
                break
        line = md.count("\n", 0, a) + 1
        items.append({
            "line": line, "quote": q, "page": page,
            "cite_author": author, "cite_year": ctx_year,
            "pos": a, "kind": kind,
        })
    items.sort(key=lambda x: x["pos"])
    return items


def match_author(cite_author, fname, aliases):
    """标注作者是否与该文件对得上。返回 (ok, 说明)。"""
    if not cite_author:
        return None, "未解析出作者"
    a = re.sub(r"[^a-z]", "", cite_author.lower())
    names = surnames_for(fname, aliases)
    if not names:
        return None, "文件名无作者信息"
    for n in names:
        if a and (a in n or n in a):
            return True, ""
    toks = surname_tokens(re.sub(r"[^a-z]", "", cite_author.lower()))
    for t in toks:
        if any(t in n for n in names):
            return True, ""
    return False, f"标注作者「{cite_author}」与该文件作者不符"


def hit_priority(fname):
    """规范命名的文件（AuthorYYYY_xxx.pdf）优先，避免同一篇的网页版/期刊版混淆页码。"""
    raw, year = file_stem_author(fname)
    return 0 if (raw and year and 2 <= len(raw) <= 20 and raw.isalpha()) else 1


def cmd_verify(args):
    md_path = Path(args.file).resolve()
    md = md_path.read_text(encoding="utf-8")
    corpus = load_corpus()
    aliases = load_aliases()
    only = set(args.only.split(",")) if args.only else None

    body_end = md.find("## 参考文献")
    body = md[:body_end] if body_end > 0 else md

    items = parse_citations(body)
    if not items:
        print("[!] 未解析到引文，检查引号或文件编码")
        return 2

    rows = []
    for it in items:
        q = it["quote"]
        if it["kind"] == "ZH":
            rows.append({
                "line": it["line"], "quote": q, "cite_author": it["cite_author"] or "",
                "cite_page": it["page"], "file": "", "page": None, "exact": "-",
                "ratio": "-", "sentence": "",
                "verdict": "ZHQUOTE",
                "note": "中文引号内的长段：若为译引，须补原文英文句与页码；否则去掉引号改为转述",
            })
            continue

        found = find_quote(corpus, q, only)
        cite_author = it["cite_author"]
        if not cite_author:
            cite_author = guess_author(body[max(0, it["pos"] - 500): it["pos"]], corpus, aliases)

        # 多份命中（重复文件/预印本与期刊版）时，优先作者能对上的、命名规范的
        actual_file, actual_page = None, None
        if found:
            cands = sorted(found.get("all_hits") or [(found["file"], found["page"])],
                           key=lambda x: (hit_priority(x[0]), x[0]))
            pick = None
            for f, p in cands:
                ok, _ = match_author(cite_author, f, aliases)
                if ok:
                    pick = (f, p)
                    break
            actual_file, actual_page = pick or cands[0]

        ratio = found["ratio"] if found else 0.0
        sentence = found["sentence"] if found else ""

        if found is None:
            verdict, note = "MISSING", "全库找不到此句，引号不成立：须删引号改写，或回原 PDF 核对"
        elif not found["exact"]:
            verdict = "PARAPHRASE"
            note = f"逐字未命中，最相似句相似度 {ratio:.2f}；引号内的句子与原文有出入"
        elif it["page"] is None:
            verdict, note = "NOPAGE", "引文逐字存在，但未标注页码"
        elif it["page"] == actual_page:
            verdict, note = "PASS", ""
        else:
            verdict = "PAGE"
            note = f"页码错：标注 p.{it['page']}，实际 p.{actual_page}"

        if found and found["exact"] and verdict in ("PASS", "PAGE", "NOPAGE"):
            auth_ok, auth_note = match_author(cite_author, actual_file, aliases)
            if auth_ok is False:
                verdict = "AUTHOR"
                note = auth_note + f"（该句实际出自 {actual_file}）"

        rows.append({
            "line": it["line"], "quote": q, "cite_author": cite_author or "",
            "cite_page": it["page"], "file": actual_file or "",
            "page": actual_page, "exact": "是" if (found and found["exact"]) else "否",
            "ratio": f"{ratio:.2f}" if found else "-",
            "verdict": verdict, "note": note, "sentence": sentence,
        })

    # 统计
    order = ["PASS", "PAGE", "AUTHOR", "PARAPHRASE", "MISSING", "NOPAGE", "ZHQUOTE"]
    stat = Counter(r["verdict"] for r in rows)
    bad = sum(v for k, v in stat.items() if k != "PASS")

    print(f"\n引文核验：{md_path.name}  共 {len(rows)} 条")
    print("=" * 78)
    for i, r in enumerate(rows, 1):
        flag = "OK " if r["verdict"] == "PASS" else "!  "
        print(f"{flag}{i:2d}. L{r['line']:<4} {r['verdict']:<11} {r['quote'][:62]}")
        if r["verdict"] != "PASS":
            print(f"      标注: {r['cite_author'] or '?'} p.{r['cite_page']}   "
                  f"实际: {r['file'] or '未找到'} p.{r['page']}")
            print(f"      {r['note']}")
            if r["sentence"] and r["verdict"] in ("PARAPHRASE", "MISSING"):
                print(f"      原文相近句: {r['sentence'][:150]}")
    print("=" * 78)
    print("汇总：" + "  ".join(f"{k}={stat[k]}" for k in order if stat[k]) + f"   合计 {len(rows)}")

    out_md = md_path.with_name(md_path.stem + "_引文核验.md")
    out_md.write_text(render_md(rows, stat, md_path.name), encoding="utf-8")
    print(f"报告：{out_md}")

    if args.xlsx:
        out_x = md_path.with_name(md_path.stem + "_引文核验.xlsx")
        write_xlsx(rows, out_x)
        print(f"表格：{out_x}")

    return 0 if bad == 0 else 1


def render_md(rows, stat, name):
    order = ["PASS", "PAGE", "AUTHOR", "PARAPHRASE", "MISSING", "NOPAGE", "ZHQUOTE"]
    lines = [f"# 引文核验报告 — {name}", ""]
    lines.append("汇总：" + "；".join(f"{k} {stat[k]}" for k in order if stat[k]))
    lines.append("")
    lines.append("| # | 行 | 判定 | 标注 | 实际 | 引文 | 说明 |")
    lines.append("|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        cite = f"{r['cite_author'] or '?'} p.{r['cite_page']}"
        real = f"{r['file'] or '—'} p.{r['page'] or '—'}"
        lines.append(f"| {i} | {r['line']} | {r['verdict']} | {cite} | {real} | "
                     f"{r['quote'][:80].replace('|', '/')} | {r['note'].replace('|', '/')} |")
    lines.append("")
    fails = [r for r in rows if r["verdict"] != "PASS"]
    if fails:
        lines.append("## 待改清单（可直接回灌给生成方）")
        lines.append("")
        for i, r in enumerate(fails, 1):
            lines.append(f"{i}. **L{r['line']} {r['verdict']}** — {r['note']}")
            lines.append(f"   - 现文：\"{r['quote'][:120]}\"")
            if r["sentence"] and r["verdict"] in ("PARAPHRASE", "MISSING"):
                lines.append(f"   - 原文：\"{r['sentence'][:200]}\"")
            lines.append("")
    return "\n".join(lines)


def write_xlsx(rows, path):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "引文核验"
    hdr = ["#", "行号", "判定", "标注作者", "标注页", "实际文件", "实际页",
           "逐字", "相似度", "引文（截断）", "原文相近句", "说明"]
    ws.append(hdr)
    for i, r in enumerate(rows, 1):
        ws.append([i, r["line"], r["verdict"], r["cite_author"], r["cite_page"],
                   r["file"], r["page"], r["exact"], r["ratio"],
                   r["quote"][:200], r["sentence"][:300], r["note"]])

    thin = Side(style="thin", color="D9D9D9")
    bd = Border(left=thin, right=thin, top=thin, bottom=thin)
    ws.freeze_panes = "C2"
    for c in ws[1]:
        c.fill = PatternFill("solid", fgColor="1F4E79")
        c.font = Font(bold=True, color="FFFFFF", size=10)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for row in ws.iter_rows(min_row=2):
        v = str(row[2].value)
        fill = None
        if v == "PASS":
            fill = PatternFill("solid", fgColor="E2EFDA")
        elif v in ("PAGE", "AUTHOR", "PARAPHRASE", "MISSING"):
            fill = PatternFill("solid", fgColor="FFC7CE")
        elif v in ("NOPAGE", "ZHQUOTE"):
            fill = PatternFill("solid", fgColor="FFEB9C")
        for c in row:
            c.alignment = Alignment(vertical="top", wrap_text=True)
            c.border = bd
            c.font = Font(size=10)
            if fill:
                c.fill = fill
    for i, w in enumerate([4, 6, 11, 18, 7, 34, 7, 6, 7, 50, 50, 46], 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    wb.save(path)


# ---------------------------------------------------------------- 抽检


ENTRY_DEF = re.compile(r"^\s*[-*]\s*论断[:：]\s*(.+?)\s*$")
ENTRY_QUOTE = re.compile(r"^\s*[-*]\s*引文[:：]\s*(.+?)\s*$")
HEADING = re.compile(r"^(#{1,6})\s*(.+?)\s*$")


def parse_note_entries(md):
    """从笔记里抽出 (命题类别, 论断, 引文行)。抽检只认这种成对结构。"""
    entries, section, pending = [], "", None
    for raw in md.splitlines():
        m = HEADING.match(raw)
        if m:
            section = m.group(2)
            pending = None
            continue
        m = ENTRY_DEF.match(raw)
        if m:
            pending = m.group(1)
            continue
        m = ENTRY_QUOTE.match(raw)
        if m and pending:
            entries.append({"section": section, "claim": pending, "quote": m.group(1)})
            pending = None
    return entries


def quote_fields(line):
    """'<引文> (Author, 2023, p.7)' -> (引文, 出处, 页)"""
    q, tail = line, ""
    m = re.match(r'^["\u201c](.+?)["\u201d]\s*(.*)$', line)
    if m:
        q, tail = m.group(1), m.group(2)
    pm = PAGE_RE.search(tail)
    page = int(pm.group(1)) if pm else None
    src = re.sub(r"[（()）]", "", tail)
    src = re.sub(r",?\s*p{1,2}\.\s*\d{1,4}.*$", "", src).strip(" ,，")
    return q, src, page


def cmd_sample(args):
    """从笔记里按固定比例、固定种子抽条目，生成可复现的闭卷审计批次。"""
    import random

    paths = []
    for p in args.path:
        p = Path(p)
        if not p.exists():
            print(f"[!] 路径不存在：{p}")
            return 2
        if p.is_dir():
            paths.extend(sorted(x for x in p.glob("*.md") if "引文核验" not in x.name))
        else:
            paths.append(p)
    if not paths:
        print("[!] 没有可抽检的笔记")
        return 1

    pool = []
    for p in paths:
        for e in parse_note_entries(p.read_text(encoding="utf-8")):
            q, src, page = quote_fields(e["quote"])
            if len(re.findall(r"[A-Za-z]", q)) < 20:      # 与 verify 同门槛，太短的它也不判
                continue
            pool.append({"doc": p.stem, "section": e["section"], "claim": e["claim"],
                         "quote": q, "src": src, "page": page})
    if not pool:
        print("[!] 未解析到「论断 + 引文」成对条目，检查笔记格式")
        return 1

    k = max(args.min, round(len(pool) * args.rate))
    k = min(k, len(pool))
    picked = sorted(random.Random(args.seed).sample(range(len(pool)), k))

    lines = [f"# 抽检批次：{args.name}", "",
             f"> 由 `python litrev.py sample` 生成，seed={args.seed}、rate={args.rate:.0%}，可复现。",
             f"> 来源 {len(paths)} 份笔记、共 {len(pool)} 条可抽条目，抽 {k} 条。",
             "> **闭卷**：只给下列五元组，不要回读原文或其它批次。", "",
             "## 合计", "",
             "| 项 | 数 |", "|---|---|", f"| 候选条目 | {len(pool)} |",
             f"| 抽检条目 | {k} |", f"| 抽检比例 | {k/len(pool):.1%} |", "",
             "## 待判条目", ""]
    for i, idx in enumerate(picked, 1):
        e = pool[idx]
        lines.append(f"### {args.prefix}{i:02d} ・ {e['doc']} ・ {e['section'] or '-'} ・ p.{e['page']}")
        lines.append("")
        lines.append(f"- 论断：{e['claim']}")
        tail = e["src"] or "?"
        lines.append(f"- 引文：\"{e['quote']}\" ({tail}, p.{e['page']})")
        lines.append("")

    text = "\n".join(lines)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"抽检 {k}/{len(pool)} 条（{k/len(pool):.1%}，seed={args.seed}）→ {out}")
    else:
        print(text)
    return 0


AUDIT_DIR = BASE / "_probe" / "audit"
SUPPORT = ("SUPPORTED", "PARTIAL", "UNSUPPORTED")
SELFSUF = ("SELF", "DEPENDENT")


def parse_audit_rows(text: str):
    """从审计输出表里取 (id, 支撑, 自足)；只认以批次号开头的表格行。"""
    rows = []
    for line in text.splitlines():
        if not re.match(r"^\|\s*[A-Z]+\d+(-\d+)?\s*\|", line):
            continue
        cell = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cell) < 3:
            continue
        rows.append((cell[0], cell[1], cell[2]))
    return rows


def cmd_audit_count(args):
    """从 out_*.md 机械汇总判定表，并校验每个文件自报的「合计」行。

    存在的理由：汇总数字手工加减已经错过两次，且错到下几份报告里。
    汇总只能由这条命令产生。
    """
    d = Path(args.dir)
    if not d.is_dir():
        print(f"[!] 目录不存在：{d}")
        return 2
    prefixes = [p.strip().upper() for p in args.prefixes.split(",") if p.strip()]
    files = []
    for p in sorted(d.glob("out_*.md")):
        m = re.match(r"^out_([A-Z]+)(\d+)\.md$", p.name)
        if m and m.group(1) in prefixes:
            files.append((m.group(1) + m.group(2), p))
    if not files:
        print("[!] 没有匹配的 out_*.md")
        return 1

    head = f"{'批次':<8}{'条数':>5}{'SUPP':>6}{'PART':>6}{'UNSU':>6}{'SELF':>6}{'DEP':>6}  合计行"
    print(head)
    print("-" * 62)
    tot = {k: 0 for k in SUPPORT}
    tot2 = {k: 0 for k in SELFSUF}
    n_all = 0
    bad = []
    for name, p in files:
        txt = p.read_text(encoding="utf-8")
        rows = parse_audit_rows(txt)
        c = {k: sum(1 for r in rows if r[1] == k) for k in SUPPORT}
        c2 = {k: sum(1 for r in rows if r[2] == k) for k in SELFSUF}
        other = [r for r in rows if r[1] not in SUPPORT or r[2] not in SELFSUF]
        for k in SUPPORT:
            tot[k] += c[k]
        for k in SELFSUF:
            tot2[k] += c2[k]
        n_all += len(rows)

        line = next((l for l in txt.splitlines() if l.startswith("合计")), "")
        mm = re.search(r"(\d+)\s*条.*?SUPPORTED\s*(\d+)\s*/\s*PARTIAL\s*(\d+)\s*/\s*"
                       r"UNSUPPORTED\s*(\d+).*?DEPENDENT\s*(\d+)", line)
        if not mm:
            mark = "缺合计行"
            bad.append(f"{name}：缺合计行")
        else:
            want = (int(mm.group(1)), int(mm.group(2)), int(mm.group(3)),
                    int(mm.group(4)), int(mm.group(5)))
            got = (len(rows), c["SUPPORTED"], c["PARTIAL"], c["UNSUPPORTED"], c2["DEPENDENT"])
            mark = "✓" if want == got else f"✗ 表内 {got[0]}/S{got[1]}/P{got[2]}/U{got[3]}/D{got[4]}"
            if want != got:
                bad.append(f"{name}：合计行 {want} ≠ 明细 {got}")
        if other:
            mark += f"  (+{len(other)} 行字段异常)"
        print(f"{name:<8}{len(rows):>5}{c['SUPPORTED']:>6}{c['PARTIAL']:>6}"
              f"{c['UNSUPPORTED']:>6}{c2['SELF']:>6}{c2['DEPENDENT']:>6}  {mark}")

    print("-" * 62)
    print(f"{'合计':<8}{n_all:>5}{tot['SUPPORTED']:>6}{tot['PARTIAL']:>6}"
          f"{tot['UNSUPPORTED']:>6}{tot2['SELF']:>6}{tot2['DEPENDENT']:>6}")
    nons = n_all - tot["SUPPORTED"]
    pct = nons / n_all * 100 if n_all else 0
    print()
    print(f"口径：{n_all} 条 · SUPPORTED {tot['SUPPORTED']} / PARTIAL {tot['PARTIAL']} / "
          f"UNSUPPORTED {tot['UNSUPPORTED']} · SELF {tot2['SELF']} / DEPENDENT {tot2['DEPENDENT']}")
    print(f"非 SUPPORTED：{nons}/{n_all} = {pct:.1f}%")
    if bad:
        print()
        print("[!] 合计行与明细不一致，报告里的数字不要照抄该文件：")
        for b in bad:
            print(f"  - {b}")
        return 1 if args.check else 0
    return 0


BATCH_IN_RE = re.compile(r"^###\s+(\S+)\s*・\s*(\S+)\s*・\s*(\S+)")
CARD_DIR = BASE / "_probe" / "full"


def parse_batch_inputs(dirpath):
    """读 FRAG_B*/REST_B* 批次输入 -> {id: {doc, sec, claim, quote, src}}。"""
    items = {}
    for p in sorted(Path(dirpath).glob("*.md")):
        if not re.match(r"^(FRAG|REST)_B\d+\.md$", p.name):
            continue
        text = p.read_text(encoding="utf-8")
        for blk in re.split(r"^### ", text, flags=re.M)[1:]:
            m = BATCH_IN_RE.match("### " + blk.splitlines()[0])
            if not m:
                continue
            q = re.search(r'^- 引文："(.+?)"\s*\(', blk, re.M)
            c = re.search(r"^- 论断：(.+)$", blk, re.M)
            items[m.group(1)] = {
                "doc": m.group(2), "sec": m.group(3),
                "claim": (c.group(1).strip() if c else ""),
                "quote": (q.group(1) if q else ""), "src": p.name,
            }
    return items


def parse_cards(dirpath):
    """读 full/*.md 卡片 -> {doc: {节名: (论断, [引文...])}}。"""
    cards = {}
    for p in sorted(Path(dirpath).glob("*.md")):
        if "引文核验" in p.name:
            continue
        text = p.read_text(encoding="utf-8")
        secs = {}
        for blk in re.split(r"^## \d+\.\s*", text, flags=re.M)[1:]:
            title = blk.splitlines()[0].strip()
            c = re.search(r"^- 论断：(.+)$", blk, re.M)
            secs[title] = (c.group(1).strip() if c else "",
                           re.findall(r'^- 引文："(.+?)"\s*\(', blk, re.M))
        cards[p.stem] = secs
    return cards


def cmd_audit_stale(args):
    """校验「判定所依据的引文/论断」是否仍是卡片当前的内容。

    存在的理由：批次输入是快照，卡片会被返工改写。快照不改，判定就悄悄变成
    「对一个已经不存在的引文做的判断」，而 audit-count 照样给出漂亮的数字。
    """
    items = parse_batch_inputs(args.audit_dir)
    cards = parse_cards(args.card_dir)
    if not items:
        print(f"[!] 没读到批次输入（{args.audit_dir}）")
        return 2

    drift, missing = [], []
    for i, it in items.items():
        secs = cards.get(it["doc"])
        if secs is None:
            missing.append((i, it["doc"], "卡片不存在"))
            continue
        got = secs.get(it["sec"])
        if got is None:
            missing.append((i, it["doc"], f"卡片无「{it['sec']}」节"))
            continue
        claim, quotes = got
        q_ok = it["quote"] in quotes
        c_ok = claim == it["claim"]
        if not (q_ok and c_ok):
            why = "引文已改" if not q_ok else ""
            if not c_ok:
                why = (why + " 论断已改").strip()
            drift.append((i, it["doc"], it["sec"], why))

    n_quote = sum(len(q) for s in cards.values() for _, q in s.values())
    n_sec = sum(len(s) for s in cards.values())
    print(f"批次输入 {len(items)} 条 · 卡片 {len(cards)} 篇 / {n_sec} 节 / {n_quote} 条引文")
    print(f"判定依据与卡片一致：{len(items) - len(drift) - len(missing)}/{len(items)}")

    if drift:
        print()
        print("表：引文或论断在判定之后被改过（这些判定作废，须重审）")
        print(f"{'id':<8}{'文献':<44}{'节':<14}变动")
        print("-" * 82)
        for i, doc, sec, why in drift:
            print(f"{i:<8}{doc[:42]:<44}{sec:<14}{why}")
    if missing:
        print()
        print("[!] 批次条目找不到对应的卡片位置：")
        for i, doc, why in missing:
            print(f"  - {i}  {doc}  {why}")

    if not drift and not missing:
        print("\n✓ 全部判定的依据与卡片当前内容一致。")
        return 0
    print(f"\n[!] {len(drift)} 条判定的依据已过期，{len(missing)} 条对不上卡片。")
    print("    重审请另建批次（不要在旧 out_*.md 上就地改判）。")
    return 1 if args.check else 0


def cmd_locate(args):
    corpus = load_corpus()
    found = find_quote(corpus, args.text)
    if not found:
        print("未找到。该表述在全库中不存在逐字来源，最接近的内容也未达阈值。")
        return 1
    print(f"文件: {found['file']}")
    print(f"PDF 页: p.{found['page']}")
    off = corpus[found["file"]].get("offset")
    if off is not None:
        print(f"印张页: p.{found['page'] + off}")
    print(f"逐字命中: {found['exact']}  相似度: {found['ratio']:.2f}")
    print(f"原句: {found['sentence']}")
    if found["all_hits"]:
        others = [f"{f} p.{p}" for f, p in found["all_hits"][1:]]
        if others:
            print("同一句在其他文件也出现（重复文件或引用转述）: " + "; ".join(others))
    return 0 if found["exact"] else 3


def match_label(label, pdfs, aliases):
    """把矩阵里的「文献」单元格匹配到库内文件。首作者权重最高，年份仅用于消歧。"""
    lab = label.lower()
    lab_key = re.sub(r"[^a-z0-9]", "", lab)
    years = set(re.findall(r"\b(?:19|20)\d{2}\b", lab))
    # 首作者区：第一个逗号/括号之前的部分
    head = re.split(r"[,，()（]| et al", lab)[0]
    head_tokens = set(re.findall(r"[a-z]{2,}", head))

    scored = []
    for f in pdfs:
        raw, yr = file_stem_author(f)
        names = surnames_for(f, aliases)
        score = 0
        is_primary = False
        for t in names:
            if t and re.search(r"\b" + re.escape(t) + r"\b", head):
                is_primary = True
                break
        if not is_primary:
            for t in list(head_tokens):
                if any(t in n for n in names) and len(t) >= 4:
                    is_primary = True
                    break
        if is_primary:
            score += 60
        # 全名或标题词命中（次级证据）
        if raw and len(raw) >= 4 and raw.lower() in lab_key:
            score += 12
        for nm in names:
            if any(len(t) >= 4 and t in lab_key for t in [nm] + surname_tokens(nm)):
                score += 8
                break
        for tok in re.findall(r"[A-Z][a-z]+|[a-z]{8,}", Path(f).stem):
            if len(tok) >= 8 and tok.lower() in lab_key:
                score += 8
                break
        if score == 0:
            continue
        if yr and str(yr) in years:
            score += 20
        scored.append((score, f))
    if not scored:
        return None, 0, 0
    scored.sort(reverse=True)
    top = scored[0][0]
    tied = sum(1 for s, _ in scored if s == top)
    return scored[0][1], top, tied


def pick_sheet(wb, hint=None):
    if hint and hint in wb.sheetnames:
        return wb[hint]
    best, best_n = None, -1
    for ws in wb.worksheets:
        rows = ws.max_row or 0
        hdr = " ".join(str(c.value) for c in ws[1] if c.value is not None) if rows else ""
        if "文献" in hdr and rows > best_n:
            best, best_n = ws, rows
    return best or wb.worksheets[0]


def cmd_matrix(args):
    import openpyxl
    wb = openpyxl.load_workbook(args.file, data_only=True)
    ws = pick_sheet(wb, args.sheet)
    rows = [r for r in ws.iter_rows(values_only=True)]
    if not rows:
        print("[!] 空表")
        return 2
    hdr = [str(c) for c in rows[0] if c is not None]
    data = [r for r in rows[1:] if any(r)]

    ci = (args.col - 1) if args.col else 0
    ci = min(ci, max(len(hdr) - 1, 0))
    names = [str(r[ci]).strip() for r in data if r[ci] is not None]

    corpus = load_corpus()
    aliases = load_aliases()
    pdfs = list(corpus)

    # 去重与扫描件：都不应计入「矩阵应有的行数」
    dup_files, scanned_files = set(), set()
    mf = IDX_DIR / "manifest.csv"
    if mf.exists():
        with open(mf, encoding="utf-8-sig") as fh:
            for row in csv.DictReader(fh):
                if row.get("duplicate_of"):
                    dup_files.add(row["file"])
                if row.get("scanned"):
                    scanned_files.add(row["file"])
    usable = [f for f in pdfs if f not in dup_files and f not in scanned_files]

    print(f"\n矩阵校验：{Path(args.file).name}   sheet={ws.title}")
    print("=" * 66)
    print(f"表头 {len(hdr)} 列：{', '.join(hdr[:10])}")
    print(f"数据行 {len(data)} 行；库内 PDF {len(pdfs)} 个 → 可校验 {len(usable)} 篇"
          f"（排除重复 {len(dup_files)}、无文字层 {len(scanned_files)}）")

    dup = [k for k, v in Counter(names).items() if v > 1]
    if dup:
        print(f"\n! 重复行（同一文献多行，会污染统计口径）：{dup}")

    matched_files, unmatched, ambiguous = set(), [], []
    for n in names:
        f, sc, tied = match_label(n, usable, aliases)
        if not f:
            unmatched.append(n)
            continue
        if tied > 1:
            ambiguous.append((n, f, tied))
        matched_files.add(f)

    print(f"\n能对上库内文件的行：{len(names) - len(unmatched)} / {len(names)}")
    if ambiguous:
        print("\n有歧义（同名作者多篇，需在单元格里写明年份）：")
        for n, f, t in ambiguous[:8]:
            print(f"  - {n[:50]}  → 同分候选 {t} 个，暂取 {Path(f).stem[:40]}")
    if unmatched:
        print("\n矩阵里有、库里没有对应文件的行（转述文献，或一篇被拆成多行）：")
        for n in unmatched[:12]:
            print(f"  - {n[:70]}")

    missing = [f for f in usable if f not in matched_files]
    if missing and args.allow_subset:
        print(f"\n（子集表：另有 {len(missing)} 篇文献未收录，按 --allow-subset 不计为缺失）")
        missing = []
    elif missing:
        print("\n库里有、矩阵里没有的行（漏收）：")
        for f in missing[:12]:
            print(f"  - {f}")

    ok = not dup and not unmatched and not missing
    print(f"\n{'✓ 通过' if ok else '! 需处理'}：行 {len(names)} / 可校验文献 {len(usable)}"
          f"（差额 {len(names)-len(usable):+d}）")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="文献综述流水线的可机械验证层")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("index", help="为 PDF 目录建索引")
    p.add_argument("--dir", default=str(PDF_DIR))
    p.set_defaults(func=cmd_index)

    p = sub.add_parser("text", help="把 PDF 逐页导出为带页标记的 txt（版面重建）")
    p.add_argument("--dir", default=str(PDF_DIR))
    p.add_argument("--out", default=None, help="输出目录（默认 litrev/_probe/texts）")
    p.add_argument("--only", default=None, help="仅处理这些文件名主干，逗号分隔")
    p.add_argument("--layout", action="store_true", default=True,
                   help="按词级坐标重建阅读顺序（默认开）")
    p.add_argument("--raw", dest="layout", action="store_false",
                   help="退回 page.get_text() 逐页直出")
    p.add_argument("--dry-run", action="store_true", help="只报健康度，不写文件")
    p.set_defaults(func=cmd_text)

    p = sub.add_parser("sample", help="按固定比例与种子抽检，生成闭卷审计批次")
    p.add_argument("path", nargs="+", help="笔记文件或目录")
    p.add_argument("--rate", type=float, default=0.12, help="抽检比例（默认 0.12）")
    p.add_argument("--min", type=int, default=1, help="至少抽几条")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--name", default="SUPPORTED 抽检", help="批次名")
    p.add_argument("--prefix", default="S", help="条目编号前缀")
    p.add_argument("--out", default=None, help="写入文件；不给则打印")
    p.set_defaults(func=cmd_sample)

    p = sub.add_parser("audit-count", help="汇总 out_*.md 判定表，并校验各文件的合计行")
    p.add_argument("--dir", default=str(AUDIT_DIR), help="审计输出目录（默认 _probe/audit）")
    p.add_argument("--prefixes", default="B,R", help="纳入的批次前缀，逗号分隔（默认 B,R）")
    p.add_argument("--check", action="store_true", help="合计行与明细不一致时以退出码 1 结束")
    p.set_defaults(func=cmd_audit_count)

    p = sub.add_parser("audit-stale", help="校验判定所依据的引文/论断是否仍是卡片当前内容")
    p.add_argument("--audit-dir", default=str(AUDIT_DIR), help="批次输入目录（默认 _probe/audit）")
    p.add_argument("--card-dir", default=str(CARD_DIR), help="卡片目录（默认 _probe/full）")
    p.add_argument("--check", action="store_true", help="存在过期判定时以退出码 1 结束")
    p.set_defaults(func=cmd_audit_stale)

    p = sub.add_parser("locate", help="回查一段文字的确切出处")
    p.add_argument("text")
    p.set_defaults(func=cmd_locate)

    p = sub.add_parser("verify", help="核验 Markdown 稿的引文")
    p.add_argument("file")
    p.add_argument("--only", default=None, help="限定文件名，逗号分隔")
    p.add_argument("--xlsx", action="store_true", help="同时输出 xlsx")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("matrix", help="校验证据矩阵 xlsx")
    p.add_argument("file")
    p.add_argument("--sheet", default=None)
    p.add_argument("--col", type=int, default=0, help="文献名列（1 起）")
    p.add_argument("--allow-subset", action="store_true",
                   help="子集表（如度量表）不要求覆盖全部文献")
    p.set_defaults(func=cmd_matrix)

    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
