#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PDF 命名建议：读前几页 / 元数据，生成 AuthorYYYY_ShortTag.pdf。

为什么默认不落盘：文件名就是引文标注 —— gen_subagents.py 靠它算 (作者, 年份)，
verify 拿它和卡片比对。猜错一个名字 = 整篇 verify 变红，已封戳卡片回不去。
所以本工具只做「建议 + 人确认」，`--apply` 才改，且有四道护栏：

  ① 已进 manifest / 已有卡片 / 已在 aliases.json 的文件名 → IN_USE，绝不改；
  ② 作者、年份、题名任一不明确，或来源只是弱启发式 → REVIEW，不猜；
  ③ 生成名与现有名、或本次其他建议撞名 → CONFLICT，不改；
  ④ 纯中文题名生成不出 ASCII ShortTag（slugify 会归成空串撞名）→ REVIEW。

用法：
  python tools/rename_pdfs.py                                   # 全库 dry-run
  python tools/rename_pdfs.py --library 1号文献库               # 只看新放的这一批
  python tools/rename_pdfs.py --library 1号文献库 --apply       # 落盘改「OK」的
  python tools/rename_pdfs.py --library 1号文献库 \
      --set "某篇原名.pdf=Jiang2024_LangchainQA" --apply        # REVIEW 项人工定名

改名留痕写 参考文献原文/_rename_log.jsonl（.gitignore 排除，不入库）。
改完必须重跑 `python litrev/litrev.py index`——corpus 以文件名为键。
"""

import argparse
import csv
import json
import re
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
PDF_ROOT = ROOT / "参考文献原文"
MANIFEST = ROOT / "litrev/_index/manifest.csv"
FULL_DIR = ROOT / "litrev/_probe/full"
ALIASES = ROOT / "litrev/aliases.json"

NORM_RE = re.compile(r"^[A-Za-z]{2,20}(19|20)\d{2}_[A-Za-z0-9_]{2,40}\.pdf$")
YEAR_RE = re.compile(r"\b((?:19|20)\d{2})\b")
CJK_RE = re.compile(r"[\u4e00-\u9fa5]")

STOPWORDS = {
    "the", "and", "for", "from", "with", "using", "used", "based", "via", "into",
    "study", "studies", "research", "analysis", "approach", "method", "methods",
    "design", "review", "survey", "towards", "toward", "case", "cases", "novel",
    "new", "paper", "article", "its", "their", "our", "this", "these", "are",
    "not", "but", "can", "of", "in", "on", "at", "to", "a", "an", "by", "as",
}
# 作者行里出现这些词就不是作者行（机构、出版信息、摘要标题）
ORG_HINTS = (
    "university", "institute", "college", "department", "school", "laboratory",
    "academy", "journal", "proceedings", "conference", "press", "elsevier",
    "springer", "ieee", "acm", "abstract", "keywords", "doi", "vol.", "pp.",
    "http", "@", "copyright", "received", "accepted", "corresponding",
)


def library_pdfs(root, library=None):
    """顶层兼容旧布局 + 一层文献库子目录；跳过 _ / . 开头的隔离区。"""
    found = [(p, "") for p in sorted(root.glob("*.pdf"))]
    for sub in sorted(root.iterdir()) if root.is_dir() else []:
        if not sub.is_dir() or sub.name.startswith(("_", ".")):
            continue
        if library and sub.name != library:
            continue
        found.extend((p, sub.name) for p in sorted(sub.glob("*.pdf")))
    if library:
        found = [t for t in found if t[1] == library]
    return found


def in_use_names():
    """已被引证链引用的文件名主干：改名会让 verify / 卡片对不上。"""
    names = set()
    if MANIFEST.exists():
        with open(MANIFEST, encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                names.add(Path(row["file"]).stem)
    if FULL_DIR.is_dir():
        names.update(p.stem for p in FULL_DIR.glob("*.md"))
    if ALIASES.exists():
        try:
            names.update(Path(k).stem for k in json.loads(ALIASES.read_text(encoding="utf-8")))
        except (ValueError, OSError):
            pass
    return names


def first_pages(doc, n):
    return "\n".join(doc[i].get_text() for i in range(min(n, len(doc))))


def ascii_surname(raw):
    toks = re.findall(r"[A-Za-z][A-Za-z'\-]*", raw)
    cand = [t for t in toks if len(t) > 1]
    if not cand:
        return ""
    s = re.sub(r"[^A-Za-z]", "", cand[-1])
    return s[:1].upper() + s[1:] if 2 <= len(s) <= 20 else ""


def author_from_meta(meta):
    raw = (meta.get("author") or "").strip()
    if not raw:
        return "", ""
    head = re.split(r"\s*(?:,|;|\band\b|&|\|)\s*", raw)[0].strip()
    s = ascii_surname(head)
    return (s, "metadata.author") if s else ("", "")


def author_from_lines(text):
    """只在强模式（A. Smith / Smith, J. / A and B）下认作者行；弱证据不自动落盘。"""
    for line in text.splitlines()[:40]:
        s = " ".join(line.split())
        if not (6 <= len(s) <= 140):
            continue
        low = s.lower()
        if any(h in low for h in ORG_HINTS) or len(CJK_RE.findall(s)) > 3:
            continue
        if not (re.search(r"[A-Z]\.\s*[A-Z][a-z]+", s)
                or re.search(r"[A-Z][a-z]+,\s*[A-Z]\.", s)
                or re.search(r"[A-Z][a-z]+\s+and\s+[A-Z][a-z]+", s)):
            continue
        head = re.split(r"\s*(?:,|;|\band\b|&)\s*", s)[0].strip()
        name = ascii_surname(head)
        if name:
            return name, "首页作者行"
    return "", ""


def year_from_text(text, meta):
    """取带出版语境的年份；并列最高分 / 只有 PDF 制作年都算证据不足。"""
    scores = Counter()
    this_year = date.today().year
    for m in YEAR_RE.finditer(text):
        y = int(m.group(1))
        if not (1950 <= y <= this_year + 1):
            continue
        ctx = text[max(0, m.start() - 45):m.end() + 45]
        score = 1
        if re.search(r"©|copyright|published|accepted|received|proceedings|"
                     r"conference|vol\.|no\.|pp\.|ieee|acm|springer|elsevier|"
                     r"\bIJ\b|journal", ctx, re.I):
            score += 2
        scores[y] += score
    if not scores:
        cd = re.search(r"D:((?:19|20)\d{2})", meta.get("creationDate") or "")
        return (int(cd.group(1)), "PDF 制作年（弱）") if cd else (None, "")
    best = max(scores.values())
    winners = [y for y, s in scores.items() if s == best]
    if len(winners) > 1:
        return None, f"年份并列 {sorted(winners)}"
    return winners[0], "首页出版语境" if best >= 3 else "首页年份（弱）"


def make_tag(title):
    words = re.findall(r"[A-Za-z][A-Za-z0-9]*", title)
    keep = [w for w in words if len(w) > 2 and w.lower() not in STOPWORDS]
    if not keep:
        return ""
    out = "".join(w[:1].upper() + w[1:].lower() for w in keep[:3])
    return re.sub(r"[^A-Za-z0-9]", "", out)[:36]


def tag_from_meta(meta):
    t = (meta.get("title") or "").strip()
    if not t or len(re.findall(r"[A-Za-z]", t)) < len(CJK_RE.findall(t)) + 4:
        return "", ""
    tag = make_tag(t)
    return (tag, "metadata.title") if tag else ("", "")


def tag_from_lines(text):
    best, best_n = "", 0
    for line in text.splitlines()[:20]:
        s = " ".join(line.split())
        low = s.lower()
        if not (18 <= len(s) <= 180) or any(h in low for h in ORG_HINTS):
            continue
        if len(CJK_RE.findall(s)) > len(re.findall(r"[A-Za-z]", s)):
            continue
        words = re.findall(r"[A-Za-z][A-Za-z0-9]*", s)
        if len(words) >= 4 and len(words) > best_n:
            tag = make_tag(s)
            if tag:
                best, best_n = tag, len(words)
    return best, "首页标题行"


def meta_corroborated(meta, text):
    """元数据必须被首页正文印证，否则只是模板 / 出版社残留，不能当高置信证据。

    实测 Jumeira 两例：Word 模板残留 title="Conference Full Paper template"、
    author="Kiky"（真实作者 Kathy Higgins）；Elsevier 章节的 metadata 是整本书的
    书名与主编（真实章节作者 Babak Hamidi）。把这类元数据当 OK 会给出错名，
    而错名就是错的引文标注。
    """
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    head = " ".join(lines[:40]).lower()
    title_head = " ".join(lines[:20]).lower()
    title = (meta.get("title") or "").lower()
    if re.search(r"template|untitled|microsoft|full paper|\.docx?\b", title):
        return False, "metadata.title 是模板/文件名残留"
    raw = (meta.get("author") or "").strip()
    if raw:
        first = re.split(r"\s*(?:,|;|\band\b|&|\|)\s*", raw)[0]
        surname = ascii_surname(first).lower()
        if surname and surname not in head:
            return False, f"metadata.author({surname}) 未在首页正文出现"
    tw = {w for w in re.findall(r"[a-z]{4,}", title) if w not in STOPWORDS}
    if title and tw and sum(1 for w in tw if w in title_head) < 2:
        return False, "metadata.title 与首页正文不印证"
    return True, ""


def propose(meta, text):
    """只算「建议名 + 证据 + 不足」，不判断 IN_USE / 撞名、不碰磁盘。

    `prepare_library.py` 的一键向导与 `main()` 共用这份判定，
    避免两处各写一套规则后偷偷漂移（错名 = 错的引文标注）。
    """
    author, a_src = author_from_meta(meta)
    if not author:
        author, a_src = author_from_lines(text)
    year, y_src = year_from_text(text, meta)
    tag, t_src = tag_from_meta(meta)
    if not tag:
        tag, t_src = tag_from_lines(text)

    evidence = (f"作者={author or '?'}({a_src or '未找到'}) "
                f"年={year or '?'}({y_src}) "
                f"题名={tag or '?'}({t_src or '未找到'})")
    issues = []
    if not author:
        issues.append("抽不到 ASCII 作者姓氏")
    if not year:
        issues.append(y_src or "抽不到年份")
    if not tag:
        issues.append("抽不到 ASCII 题名词（中文题名请人工定名）")
    if "弱" in y_src or a_src == "首页作者行" or t_src == "首页标题行":
        issues.append("证据来自启发式而非元数据")
    corroborated, why = meta_corroborated(meta, text)
    if not corroborated:
        issues.append(why + "（按首页正文人工定名）")

    new = f"{author}{year}_{tag}.pdf" if author and year and tag else "-"
    return new, evidence, issues


def parse_sets(items):
    out = {}
    for item in items or []:
        if "=" not in item:
            sys.exit(f"[!] --set 要写成 原名.pdf=标准名，收到：{item}")
        old, new = item.split("=", 1)
        new = new.strip()
        if not new.endswith(".pdf"):
            new += ".pdf"
        if not NORM_RE.fullmatch(new):
            sys.exit(f"[!] --set 给的名字不合规范 AuthorYYYY_Tag.pdf：{new}")
        out[old.strip()] = new
    return out


def main():
    ap = argparse.ArgumentParser(description="PDF 命名建议（默认只看不改）")
    ap.add_argument("--dir", default=str(PDF_ROOT), help="文献库根目录")
    ap.add_argument("--library", default=None, help="只看某个文献库子目录")
    ap.add_argument("--pages", type=int, default=2, help="读前几页（默认 2）")
    ap.add_argument("--apply", action="store_true", help="落盘改状态为 OK / 人工定名的条目")
    ap.add_argument("--set", dest="sets", action="append", metavar="原名.pdf=标准名",
                    help="人工给 REVIEW 项定名，可重复")
    args = ap.parse_args()

    import pymupdf

    root = Path(args.dir).resolve()
    log_path = root / "_rename_log.jsonl"
    entries = library_pdfs(root, args.library)
    if not entries:
        print(f"[!] {root} 下没有匹配的 PDF"
              + (f"（文献库 {args.library}）" if args.library else ""))
        return 1

    used = in_use_names()
    existing = {p.name for p, _ in library_pdfs(root)}
    overrides = parse_sets(args.sets)
    rows, changed, log_rows = [], 0, []
    proposed = {}

    for path, lib in entries:
        name = path.name
        if name in overrides:
            new = overrides[name]
            rows.append(("人工定名", lib, name, new, "--set 指定", ""))
            proposed[new] = name
            if args.apply and not (path.parent / new).exists():
                path.rename(path.parent / new)
                changed += 1
                log_rows.append({"library": lib, "old": name, "new": new,
                                 "status": "MANUAL", "evidence": "--set"})
            continue

        if path.stem in used:
            rows.append(("IN_USE", lib, name, "-", "已进 manifest/卡片/别名，不许改名", ""))
            continue
        if NORM_RE.fullmatch(name):
            rows.append(("已规范", lib, name, "-", "已符合 AuthorYYYY_Tag.pdf", ""))
            continue

        try:
            doc = pymupdf.open(path)
        except Exception as e:
            rows.append(("打不开", lib, name, "-", str(e)[:60], ""))
            continue
        try:
            meta = doc.metadata or {}
            text = first_pages(doc, args.pages)
        finally:
            doc.close()

        new, evidence, issues = propose(meta, text)

        if issues:
            status, note = "REVIEW", "；".join(issues)
        elif new in existing or new in proposed:
            status, note = "CONFLICT", f"与现有/本次建议撞名（{proposed.get(new, '已存在')}）"
        elif not NORM_RE.fullmatch(new):
            status, note = "REVIEW", "生成名不合规范"
        else:
            status, note = "OK", ""
            proposed[new] = name

        rows.append((status, lib, name, new, evidence, note))

        if args.apply and status == "OK":
            path.rename(path.parent / new)
            changed += 1
            log_rows.append({"library": lib, "old": name, "new": new,
                             "status": "AUTO", "evidence": evidence})
            existing.add(new)

    print(f"文献库根：{root}" + (f" · 限定库：{args.library}" if args.library else ""))
    print(f"扫描 {len(entries)} 篇 PDF；模式：{'APPLY（已落盘）' if args.apply else 'DRY-RUN（不改文件）'}")
    print("=" * 110)
    for status, lib, old, new, ev, note in rows:
        print(f"[{status:8s}] {lib or '(根)'} | {old}")
        if new != "-":
            print(f"             → {new}")
        print(f"             {ev}")
        if note:
            print(f"             ⚠ {note}")

    n = Counter(r[0] for r in rows)
    print("=" * 110)
    print("状态汇总：" + "  ".join(f"{k}={v}" for k, v in sorted(n.items())))

    if args.apply:
        if log_rows:
            with open(log_path, "a", encoding="utf-8") as fh:
                for rec in log_rows:
                    rec["ts"] = datetime.now().isoformat(timespec="seconds")
                    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"已改名 {changed} 篇；留痕 {log_path}")
        if changed:
            print("下一步必做：python litrev/litrev.py index → text --library <库名> → gen_subagents.py")
        if any(r[0] in ("REVIEW", "CONFLICT") for r in rows):
            print("仍有 REVIEW/CONFLICT：用 --set '原名.pdf=AuthorYYYY_Tag' 人工定名后再 --apply")
    else:
        print("确认无误后加 --apply；REVIEW/CONFLICT 项用 --set 人工定名，本工具不会替你猜。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
