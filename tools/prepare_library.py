#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""「机器侧准备」一键向导：命名 → 文字层体检 → index → text → 生成 ex- 子代理。

由项目根目录的 `准备文献库.bat` 调用；`--plan` 只做只读预检。

为什么需要这道向导（都是实测过的约束，不是流程洁癖）：
  ① `index` 是**全库清空重建**，动手前必须保证所有非隔离库的文件名合规、
     跨库无同名，否则已有卡片的引文会查不到、corpus 键会互相覆盖；
  ② 文件名就是引文标注（`gen_subagents.py` 靠它算作者/年份，`verify` 拿它比对），
     所以命名只给建议，`REVIEW` 一律由人给名，猜错等于整篇卡片作废；
  ③ 新 agent 只在 OpenCode 客户端启动时进注册表，脚本结束时必须**人重启客户端**。

本脚本绝不改 `litrev/litrev.py`、契约、卡片、判定表；只动 PDF 文件名/位置、
由 index/text/gen 生成的中间产物。写坏的 manifest/corpus 会自动回滚。
"""

import argparse
import csv
import io
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import rename_pdfs as rp  # noqa: E402  命名判定单源
sys.path.insert(0, str(ROOT / "litrev"))
import litrev  # noqa: E402  复用 iter_library_pdfs 的跨库同名拦截

PDF_ROOT = ROOT / "参考文献原文"
MANIFEST = ROOT / "litrev/_index/manifest.csv"
CORPUS = ROOT / "litrev/_index/corpus.json.gz"
TEXTS = ROOT / "litrev/_probe/texts"
FULL = ROOT / "litrev/_probe/full"
ALIASES = ROOT / "litrev/aliases.json"
MAP_FILE = ROOT / "litrev/_probe/AGENT_MAP.md"
REJECTED = PDF_ROOT / "_rejected"
PARKED = PDF_ROOT / "_parked"
TOP = "(根目录)"

YES = False
PLAN = False


# ---------------------------------------------------------------- 基础工具

def fail(msg):
    raise SystemExit(f"\n[×] {msg}")


def ask(prompt, default=""):
    interactive = sys.stdin.isatty()
    try:
        s = input(prompt).strip()
    except EOFError:
        # 交互输入意外结束：绝不猜文件名、绝不继续跑 index。
        if not interactive:
            print()
        fail("交互输入结束 —— 为安全起见已中止（此时尚未改动任何文件）")
    if not interactive:
        print()  # 管道喂输入时终端不回显，补换行避免提示与后续输出粘连
    return s or default


def confirm(question, default=True):
    if YES:
        print(f"{question} → {'是' if default else '否'}（--yes）")
        return default
    s = ask(question + (" [Y/n] " if default else " [y/N] ")).lower()
    return default if not s else s in ("y", "yes", "是")


def run(argv, quiet=False):
    """子进程统一 UTF-8 + errors=replace：Windows 控制台中文 / sys.exit(中文) 都不炸。"""
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    p = subprocess.run([sys.executable, *argv], cwd=str(ROOT), env=env,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    out = (p.stdout or "") + (p.stderr or "")
    if not quiet:
        print(out.rstrip())
    return p.returncode, out


def lib_pdfs():
    """{库名: [PDF]}；下划线/点开头的是隔离区，不参与扫描。"""
    out = {}
    top = sorted(PDF_ROOT.glob("*.pdf"))
    if top:
        out[TOP] = top
    if PDF_ROOT.is_dir():
        for sub in sorted(PDF_ROOT.iterdir()):
            if sub.is_dir() and not sub.name.startswith(("_", ".")):
                pdfs = sorted(sub.glob("*.pdf"))
                if pdfs:
                    out[sub.name] = pdfs
    return out


def in_use():
    """已被引证链引用的文件名主干：这些名字不许被新文献占用。"""
    names = set()
    if MANIFEST.exists():
        txt = MANIFEST.read_text(encoding="utf-8-sig", errors="replace")
        for r in csv.DictReader(io.StringIO(txt)):
            names.add(Path(r.get("file", "")).stem)
    if FULL.is_dir():
        names.update(p.stem for p in FULL.glob("*.md"))
    if ALIASES.exists():
        try:
            names.update(Path(k).stem for k in json.loads(ALIASES.read_text(encoding="utf-8")))
        except (ValueError, OSError):
            pass
    return names


def classify(path, used):
    if path.stem in used:
        return "已入库"
    if rp.NORM_RE.fullmatch(path.name):
        return "新·已规范"
    return "需定名"


def show_scan(libs, used):
    print("\n当前文献库（隔离区不计）：")
    print(f"  {'库名':24s} {'PDF':>4s} {'已入库':>6s} {'新·已规范':>9s} {'需定名':>6s}")
    for name, pdfs in libs.items():
        c = {"已入库": 0, "新·已规范": 0, "需定名": 0}
        for p in pdfs:
            c[classify(p, used)] += 1
        print(f"  {name[:24]:24s} {len(pdfs):4d} {c['已入库']:6d} "
              f"{c['新·已规范']:9d} {c['需定名']:6d}")
    if not libs:
        print("  （空）")


# ---------------------------------------------------------------- 1. 选库

def choose_library(libs, used, explicit=None):
    fresh = [n for n, ps in libs.items()
             if any(classify(p, used) != "已入库" for p in ps)]
    if explicit:
        if explicit not in libs:
            fail(f"没有这个文献库：{explicit}（可用：{', '.join(libs) or '无'}）")
        return explicit
    if not fresh:
        return None
    if len(fresh) == 1 or PLAN:
        chosen = fresh[0]
        print(f"\n本次入库库：{chosen}"
              + ("（--plan 预览，未提问）" if PLAN else "（只有一个库含新文献，自动选定）"))
        return chosen
    print("\n含新文献的库：")
    for i, n in enumerate(fresh, 1):
        print(f"  {i}. {n}（{len(libs[n])} 篇）")
    s = ask(f"选哪个库？[1-{len(fresh)}，回车=1] ", "1")
    try:
        idx = int(s)
    except ValueError:
        idx = 1 if s in fresh else 0
    if not (1 <= idx <= len(fresh)):
        fail("选库无效，已中止")
    return fresh[idx - 1]


# ---------------------------------------------------------------- 2. 命名

def suggest(path):
    import pymupdf
    try:
        doc = pymupdf.open(path)
    except Exception as e:
        return "-", str(e)[:80], ["PDF 打不开"]
    try:
        meta = doc.metadata or {}
        text = rp.first_pages(doc, 2)
    finally:
        doc.close()
    return rp.propose(meta, text)


def load_names_file(lib, targets, taken):
    """可选的批量定名清单：参考文献原文/<库名>/_names.txt，每行 原名.pdf=AuthorYYYY_Tag。

    把「开卷查期刊年份」这一步前置成一份人工清单，向导就能零提问跑完。
    清单只覆盖本库待定名的文件；不合规/撞名/对不上原名的行只提示、不落盘。
    """
    f = PDF_ROOT / lib / "_names.txt"
    if not f.exists():
        return {}
    target_names = {p.name for p in targets}
    out = {}
    for ln, line in enumerate(f.read_text(encoding="utf-8-sig", errors="replace").splitlines(), 1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if "=" not in s:
            print(f"  [提示] _names.txt 第 {ln} 行缺 '='，忽略：{s[:40]}")
            continue
        old, new = (x.strip() for x in s.split("=", 1))
        if not new.endswith(".pdf"):
            new += ".pdf"
        if old not in target_names:
            print(f"  [提示] 清单里的 {old[:40]} 不是本库待定名文件，忽略")
            continue
        if not rp.NORM_RE.fullmatch(new) or new in taken:
            print(f"  [提示] 清单里的 {new} 格式不对或撞名，忽略")
            continue
        out[old] = new
        taken.add(new)
    return out


def name_batch(lib, pdfs, used, libs):
    """逐篇确认命名。返回 (overrides, parked)。不在这里落盘。"""
    targets = [p for p in pdfs if classify(p, used) == "需定名"]
    if not targets:
        print("\n✓ 本库文件名全部符合 AuthorYYYY_Tag.pdf，无需定名")
        return {}, []
    print(f"\n本库有 {len(targets)} 篇文件名不合规范，逐篇确认：")
    taken = {p.name for ps in libs.values() for p in ps}
    taken |= {n + ".pdf" for n in used}
    overrides, parked = {}, []

    preset = load_names_file(lib, targets, taken)
    if preset:
        print(f"  ✓ 已读 `{lib}/_names.txt` 的人工定名 {len(preset)} 条（这些篇不再提问）")
        overrides.update(preset)
        targets = [p for p in targets if p.name not in preset]
        if not targets:
            if PLAN:
                print("  [plan] 清单覆盖全部待定名篇，运行时零提问")
            return overrides, parked

    for p in targets:
        new, evidence, issues = suggest(p)
        ok = (new != "-" and not issues and rp.NORM_RE.fullmatch(new)
              and new not in taken)
        print("-" * 78)
        print(f"  {p.name}")
        print(f"  {evidence}")
        if issues:
            print(f"  ⚠ {'；'.join(issues)}")
        print(f"  建议：{new if new != '-' else '(给不出)'}   "
              f"{'[可采纳]' if ok else '[须人工定名]'}")

        if PLAN:
            print("  [plan] 运行时此处会请你输入标准名 / a 采纳 / s 暂不入库")
            continue
        while True:
            s = ask("  → 标准名 或 a(采纳) / s(暂不入库) / q(中止)：")
            if s.lower() in ("q", "quit", "exit"):
                fail("已中止；此时尚未改动任何文件")
            if s.lower() == "s":
                parked.append(p)
                break
            if s.lower() == "a":
                if not ok:
                    print("    这条不能采纳（证据不足或撞名），请直接输入标准名")
                    continue
                overrides[p.name] = new
                taken.add(new)
                break
            cand = s if s.endswith(".pdf") else s + ".pdf"
            if not rp.NORM_RE.fullmatch(cand):
                print("    格式不对：必须是 AuthorYYYY_ShortTag.pdf（如 Smith2024_ShearWall）")
                continue
            if cand in taken:
                print("    这个名字已被占用（现有 PDF / 已入库标注），换一个")
                continue
            overrides[p.name] = cand
            taken.add(cand)
            break

    if PLAN:
        return {}, []
    return overrides, parked


def apply_naming(lib, overrides, parked):
    if parked:
        PARKED.mkdir(parents=True, exist_ok=True)
        for p in parked:
            dst = PARKED / p.name
            if dst.exists():
                dst = PARKED / f"{p.stem}_{datetime.now():%H%M%S}{p.suffix}"
            shutil.move(str(p), str(dst))
            print(f"  暂不入库 → {dst.relative_to(ROOT)}")
    if overrides:
        argv = ["tools/rename_pdfs.py", "--dir", str(PDF_ROOT),
                "--library", lib, "--apply"]
        for old, new in overrides.items():
            argv += ["--set", f"{old}={new}"]
        rc, _ = run(argv)
        if rc:
            fail("改名工具失败，已中止（不要手工改文件名，先看上面的原因）")
    # 复检：本库不该再有「需定名」
    used = in_use()
    left = [p.name for p in (PDF_ROOT / lib).glob("*.pdf")
            if classify(p, used) == "需定名"]
    if left:
        fail(f"仍有不合规文件名：{'、'.join(left)}")


# ---------------------------------------------------------------- 3. 全库预检

def global_precheck(used, lib):
    """index 是全库清空重建：其它库里若有不合规新文件，必须先处理。"""
    try:
        entries = litrev.iter_library_pdfs(PDF_ROOT)  # 跨库同名会 sys.exit
    except SystemExit as e:
        fail(str(e))
    bad = [(p, l or TOP) for p, l in entries
           if p.stem not in used and not rp.NORM_RE.fullmatch(p.name)]
    outside = [(p, l) for p, l in bad if l != lib]
    if not outside:
        print("\n✓ 全库预检通过：跨库无同名，其它库没有不合规的新文件")
        return
    names = sorted({l for _, l in outside})
    print(f"\n[!] 其它 {len(names)} 个库里还有 {len(outside)} 篇不合规新文件：")
    for n in names:
        cnt = sum(1 for _, l in outside if l == n)
        print(f"    {n}: {cnt} 篇（例：{next(p.name for p, l in outside if l == n)[:46]}）")
    if TOP in names:
        fail("顶层还留着 PDF（旧布局）。请把它们移进 `参考文献原文/<库名>/` 再运行")
    libs = lib_pdfs()
    unsafe = [n for n in names
              if any(p.stem in used for p in libs.get(n, []))]
    if unsafe:
        fail(f"这些库含已入库文献，不能隔离：{'、'.join(unsafe)}。请先给其中的新 PDF 定名")
    if PLAN:
        print("  [plan] 运行时会询问是否把这些库临时隔离（目录名前加 '_'，可逆）")
        return
    if not confirm(f"  把它们临时隔离？（改名 _<库名>，不删文件、随时改回）", True):
        fail("已中止：带着不合规文件名跑 index 会污染 manifest")
    for n in names:
        src, dst = PDF_ROOT / n, PDF_ROOT / ("_" + n)
        if dst.exists():
            fail(f"隔离目标已存在：{dst.name}；先手工处理这个目录")
        src.rename(dst)
        print(f"  已隔离 {n} → {dst.name}")


# ---------------------------------------------------------------- 4. 文字层

def parse_bullets(out, header_start):
    bad, collect = [], False
    for line in out.splitlines():
        if line.startswith(header_start):
            collect = True
            continue
        if collect:
            m = re.match(r"^\s*-\s+(.+?)\s*$", line)
            if m:
                # gen_subagents.py 的「未生成」行是 `  - 文献：原因`，中文冒号不是空白；
                # 先取整行再切冒号，带空格的文件名也不会被截断。
                bad.append(m.group(1).split("：")[0].split(":")[0].strip())
            elif line.strip():
                collect = False
    return bad


def text_check(lib):
    argv = ["litrev/litrev.py", "text", "--library", lib, "--dry-run"]
    rc, out = run(argv)
    if rc:
        fail("文字层体检命令失败")
    bad = parse_bullets(out, "[!] 版面重建后仍低于")
    if not bad:
        print("\n✓ 文字层体检通过（dry-run，未写 txt）")
        return
    print(f"\n[!] {len(bad)} 篇文字层坏到不能按行取句：{'、'.join(bad)}")
    if PLAN:
        print("  [plan] 运行时会询问是否移进 _rejected/（不删文件）")
        return
    if not confirm("  移进 _rejected/ 隔离区？", True):
        fail("已中止：文字层不可用的 PDF 会产出废卡片")
    REJECTED.mkdir(parents=True, exist_ok=True)
    for stem in bad:
        p = PDF_ROOT / lib / (stem + ".pdf")
        if not p.exists():
            fail(f"找不到 {p}，可能被改名过；请手工核对")
        shutil.move(str(p), str(REJECTED / p.name))
        print(f"  已隔离 → {REJECTED.name}/{p.name}")
    rc, out = run(argv)
    if rc or parse_bullets(out, "[!] 版面重建后仍低于"):
        fail("隔离后仍有文字层坏件，已中止")


# ---------------------------------------------------------------- 5. index + 回滚护栏

def snapshot():
    return (MANIFEST.read_bytes() if MANIFEST.exists() else None,
            CORPUS.read_bytes() if CORPUS.exists() else None)


def restore(snap):
    m, c = snap
    if m is None:
        MANIFEST.unlink(missing_ok=True)
    else:
        MANIFEST.write_bytes(m)
    if c is None:
        CORPUS.unlink(missing_ok=True)
    else:
        CORPUS.write_bytes(c)


def manifest_rows(blob):
    if blob is None:
        return {}
    txt = blob.decode("utf-8-sig", errors="replace")
    return {r.get("file", ""): r for r in csv.DictReader(io.StringIO(txt))}


# 只有「条目消失 / 页数变化 / 去重关系变化」会让已有卡片定位到错误的地方。
# words_per_line、short_line_ratio、chars、scanned、fragmented 都是对 PDF 文字层的
# 统计量，换 PyMuPDF 版本就会重算出不同的小数（实测 1.28.2 与 2.0 差 4.26 → 4.35），
# 拿它们当「PDF 被换过」的证据会误拦。真正的判据是 index 后 verify 全库能否逐字命中。
HARD_FIELDS = ("pages", "duplicate_of")


def check_manifest(before):
    old = manifest_rows(before[0])
    now = MANIFEST.read_bytes() if MANIFEST.exists() else None
    new = manifest_rows(now)
    missing = sorted(set(old) - set(new))
    hard, drift = [], []
    for k, r in old.items():
        if k not in new:
            continue
        for f, v in r.items():
            nv = new[k].get(f)
            if nv == v:
                continue
            (hard if f in HARD_FIELDS else drift).append((k, f, v, nv))
    return missing, hard, drift, len(old)


def do_index():
    print("\n即将全库清空重建 manifest.csv / corpus.json.gz。"
          "硬校验：已有条目不消失、页数/去重关系不变；"
          "随后用 verify 全库确认引文仍逐字命中，任一不过自动回滚。")
    if PLAN:
        print("  [plan] 将执行：python litrev/litrev.py index")
        return
    if not confirm("  继续？", True):
        fail("已中止，未重建索引")
    snap = snapshot()
    rc, _ = run(["litrev/litrev.py", "index"])
    if rc:
        restore(snap)
        fail("index 失败，已恢复重建前的 manifest/corpus")
    missing, hard, drift, n_old = check_manifest(snap)
    if missing or hard:
        restore(snap)
        fail(f"index 动了已有条目的身份（消失 {len(missing)} 条 / 硬变化 {len(hard)} 处），"
             f"已自动回滚。先看：{missing[:3]} {hard[:3]}")
    if drift:
        print(f"  [提示] {len(drift)} 处统计列重算漂移（例：{drift[:2]}）；"
              f"通常是当前解释器的 PyMuPDF 版本与索引基准不同，不是 PDF 被换")

    # 真正的放行判据：新 corpus 下已有卡片的引文是否仍逐字命中。
    # 这比「比 manifest 里的小数」严格得多，也不会被依赖版本差异误伤。
    sys.path.insert(0, str(ROOT / "tools"))
    import check
    tp, tq, bad = check.verify_all()
    if bad or tq == 0 or tp != tq:
        restore(snap)
        fail(f"index 后 verify 全库 {tp}/{tq}，未全绿（{bad[:3]}）；已回滚。"
             f"多半是当前解释器的 PyMuPDF 与索引基准不一致 —— "
             f"用环境变量 LITREV_PYTHON 指定生成基准的解释器后重跑")
    print(f"✓ index 重建完成；已有 {n_old} 条未消失、页数未变；"
          f"verify 全库 {tp}/{tq} PASS（用当前解释器复核）")


# ---------------------------------------------------------------- 6. text / gen

def do_text_and_gen(lib):
    if PLAN:
        print("  [plan] 将执行：python litrev/litrev.py text --library <库名>")
        print("  [plan] 将执行：python tools/gen_subagents.py && --check")
        return
    rc, _ = run(["litrev/litrev.py", "text", "--library", lib])
    if rc:
        fail("导出 txt 失败")
    all_stems = {p.stem for p, _ in litrev.iter_library_pdfs(PDF_ROOT)}
    orphan = sorted({p.stem for p in TEXTS.glob("*.txt")} - all_stems)
    if orphan:
        print(f"  [提示] {len(orphan)} 个 txt 没有对应 PDF（历史残留，本脚本不自动删）："
              f"{'、'.join(orphan[:5])}")

    rc, out = run(["tools/gen_subagents.py"])
    if rc:
        fail("生成子代理失败")
    skipped = parse_bullets(out, "未生成（这些文献不该派抽取工）")
    if skipped:
        print(f"  [提示] {len(skipped)} 篇未生成抽取工：{'、'.join(skipped)}")
    rc, _ = run(["tools/gen_subagents.py", "--check"])
    if rc:
        fail("gen --check 未通过，不要派发")


def ex_names(lib):
    if not MAP_FILE.exists():
        return []
    text = MAP_FILE.read_text(encoding="utf-8")
    names = []
    for p in sorted((PDF_ROOT / lib).glob("*.pdf")):
        m = re.search(r"^\|\s*`" + re.escape(p.stem) + r"`\s*\|\s*([^|]+)\|",
                      text, re.M)
        if m:
            hit = re.findall(r"`([^`]+)`", m.group(1))
            if hit:
                names.append(hit[0])
    return names


# ---------------------------------------------------------------- 主流程

def main():
    global YES, PLAN
    ap = argparse.ArgumentParser(description="机器侧准备一键向导")
    ap.add_argument("--library", help="跳过选库提问，直接指定文献库名")
    ap.add_argument("--plan", action="store_true", help="只读预检：不提问、不写盘、不改名")
    ap.add_argument("--yes", action="store_true", help="所有确认按默认值自动通过")
    args = ap.parse_args()
    YES, PLAN = args.yes, args.plan

    print("=" * 78)
    print("Litreview · 机器侧准备向导" + ("（--plan 只读预检）" if PLAN else ""))
    print("=" * 78)

    if not PDF_ROOT.is_dir():
        fail(f"找不到文献库根目录：{PDF_ROOT}")
    try:
        import pymupdf
    except ImportError:
        fail("缺依赖 pymupdf：先跑 pip install pymupdf")
    print(f"运行环境：Python {sys.version.split()[0]} · "
          f"PyMuPDF {getattr(pymupdf, 'VersionBind', '?')} · {sys.executable}")
    print("（版面统计随 PyMuPDF 版本变化；索引是否安全由 index 后的 verify 全库裁决，"
          "要固定解释器可设 LITREV_PYTHON）")
    for f in ("litrev/litrev.py", "tools/gen_subagents.py", "tools/rename_pdfs.py",
              "litrev/_probe/AGENT_ROLES.md"):
        if not (ROOT / f).exists():
            fail(f"项目文件缺失：{f}（请在完整 clone 里运行）")

    used = in_use()
    libs = lib_pdfs()
    show_scan(libs, used)
    lib = choose_library(libs, used, args.library)
    if lib is None:
        print("\n没有新文献：本库不跑 index 也不会有新 ex- 子代理。"
              "如果只想重建，请加 --library <库名> 显式指定。")
        return 0
    if lib == TOP:
        fail("顶层 PDF 是旧布局：请把它们移进 `参考文献原文/<库名>/` 再运行")

    overrides, parked = name_batch(lib, libs[lib], used, libs)
    if not PLAN:
        apply_naming(lib, overrides, parked)

    global_precheck(in_use(), lib)
    text_check(lib)
    do_index()
    do_text_and_gen(lib)

    if PLAN:
        print("\n" + "=" * 78)
        print("--plan 结束：未写盘、未改名、未移动任何文件。")
        print("去掉 --plan（或直接双击根目录 bat）即真正执行上面的步骤。")
        return 0

    names = ex_names(lib)
    print("\n" + "=" * 78)
    print("机器侧准备完成。接下来只做人做的三件事：")
    print("  1) 重启 OpenCode 客户端 —— 新 ex- 只在启动时进注册表，不重启会报 Unknown agent type")
    print("  2) 在客户端同一条消息里并列派以下 task（名字从 AGENT_MAP.md 抄，别凭记忆）：")
    if names:
        for n in names:
            print(f"       task  @{n}")
    else:
        print("       （本库没有新 ex-：卡片可能已存在，去 AGENT_MAP.md 核对）")
    print("  3) 卡片回来后建批次 → 生成 auditor-<批次> → 那一次还要再重启一次")
    print("\n文字层只做了 wpl 机械预检；按 PRODUCTION.md §二·二 人眼看一遍首页"
          "（字符可读性 → 句子连续性），这一步向导不替代。")
    print("此刻 check.py 若红几项属「备料态」，不要修、不要补占位 out_*.md。")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
