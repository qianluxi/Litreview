#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
litrev — 文献综述流水线的可机械验证层

设计原则（对应 loop 的三个必要部件）：
  1) 完成条件可机械判定：引文逐字命中 / 页码正确 / 作者匹配 / 矩阵行数=文献数
  2) 生成与校验分离：本工具只判定，不改写正文
  3) 失败可见：每条给出「标注 vs 实际」，便于回灌给生成方

子命令：
  index    为 PDF 目录建索引（页级文本 + 印张页码偏移 + 重复/扫描件识别）
  locate   给一段（可能是转述的）文字，找回它在原文中的确切句子与页码
  verify   扫描 Markdown 稿，核对每条引文与每条引用标注
  matrix   校验证据矩阵 xlsx：行数、篇目对应、重复、缺失

用法示例：
  python litrev.py index
  python litrev.py locate "knowledge available to adapt old solutions"
  python litrev.py verify ../notes/文献综述_初稿_v1.md
  python litrev.py matrix ../notes/证据矩阵_v2_定稿.xlsx
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

        pages, keys = [], []
        for i, pg in enumerate(doc):
            k = key_of(pg.get_text())
            keys.append(k)
            pages.append({"p": i + 1, "k": k})

        total_chars = sum(len(k) for k in keys)
        empty = sum(1 for k in keys if len(k) < 50)
        offset = detect_printed_offset(doc)

        sig = key_of("".join(keys[:2]))[:5000]
        corpus[f.name] = {"pages": pages, "offset": offset, "n": len(pages)}
        sigs[f.name] = sig
        manifest.append({
            "file": f.name,
            "pages": len(pages),
            "chars": total_chars,
            "empty_pages": empty,
            "printed_offset": "" if offset is None else offset,
            "scanned": "是" if total_chars < len(pages) * 120 else "",
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
    print(f"索引完成：{len(manifest)} 个 PDF，去重后 {len(uniq)} 篇，共 {sum(m['pages'] for m in manifest)} 页")
    print(f"索引文件：{IDX_FILE}  ({IDX_FILE.stat().st_size/1e6:.1f} MB)")
    if scanned:
        print("\n无文字层 / 抽取几乎为空（必须 OCR 或人工核对，不可交给自动校验）：")
        for m in scanned:
            print(f"  - {m['file']}  ({m['pages']} 页，仅 {m['chars']} 字符)")
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
            if qkey in pg["k"]:
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
