#!/usr/bin/env python3
"""納品前の機械走査。

Markdown / テキスト / docx / pptx / xlsx からテキストを取り出し、
置き換え済みのはずの表現が残っていないかを走査する。
標準ライブラリだけで動く（python-pptx 等は不要）。

    python3 scan_expressions.py 提出予定のフォルダ
    python3 scan_expressions.py deck.pptx --add "プロジェクト固有の語"
    python3 scan_expressions.py . --patterns 別のpatterns.json
"""
import argparse
import json
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TEXT_EXT = {".md", ".txt", ".csv", ".html", ".json"}
OOXML = {".docx": ("word/", "w:t"), ".pptx": ("ppt/slides/", "a:t"), ".xlsx": (None, None)}
TAG = re.compile(r"<[^>]+>")


def strip_tags(xml: str) -> str:
    xml = re.sub(r"</a:p>|</w:p>|<w:br/>|<a:br/>", "\n", xml)
    return TAG.sub("", xml)


def read_ooxml(path: str, ext: str):
    """(ラベル, テキスト) を返す。ラベルはシート名やスライド番号。"""
    out = []
    try:
        z = zipfile.ZipFile(path)
    except Exception as e:
        return [("", "[読めません: %s]" % e)]
    names = z.namelist()
    if ext == ".pptx":
        slides = sorted(
            (n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)),
            key=lambda n: int(re.search(r"(\d+)", n).group(1)),
        )
        for n in slides:
            num = re.search(r"(\d+)", n).group(1)
            out.append(("スライド%s" % num, strip_tags(z.read(n).decode("utf-8", "ignore"))))
        for n in names:
            if n.startswith("ppt/notesSlides/"):
                out.append((os.path.basename(n), strip_tags(z.read(n).decode("utf-8", "ignore"))))
    elif ext == ".docx":
        for n in names:
            if n.startswith("word/") and n.endswith(".xml") and "document" in n or n.startswith("word/comments"):
                out.append((os.path.basename(n), strip_tags(z.read(n).decode("utf-8", "ignore"))))
    elif ext == ".xlsx":
        shared = []
        if "xl/sharedStrings.xml" in names:
            raw = z.read("xl/sharedStrings.xml").decode("utf-8", "ignore")
            shared = [strip_tags(m) for m in re.findall(r"<si>(.*?)</si>", raw, re.S)]
        sheet_names = []
        if "xl/workbook.xml" in names:
            wb = z.read("xl/workbook.xml").decode("utf-8", "ignore")
            sheet_names = re.findall(r'<sheet[^>]*name="([^"]*)"', wb)
        idx = 0
        for n in sorted(n for n in names if re.match(r"xl/worksheets/sheet\d+\.xml$", n)):
            label = sheet_names[idx] if idx < len(sheet_names) else os.path.basename(n)
            idx += 1
            raw = z.read(n).decode("utf-8", "ignore")
            lines = []
            for cell in re.findall(r"<c[^>]*r=\"([A-Z]+\d+)\"[^>]*t=\"s\"[^>]*>\s*<v>(\d+)</v>", raw):
                ref, si = cell
                if int(si) < len(shared):
                    lines.append("%s\t%s" % (ref, shared[int(si)]))
            for cell in re.findall(r"<c[^>]*r=\"([A-Z]+\d+)\"[^>]*>\s*<is>(.*?)</is>", raw, re.S):
                lines.append("%s\t%s" % (cell[0], strip_tags(cell[1])))
            out.append((label, "\n".join(lines)))
        for n in names:
            if n.startswith("xl/comments") or n.startswith("xl/threadedComments"):
                out.append(("コメント:" + os.path.basename(n),
                            strip_tags(z.read(n).decode("utf-8", "ignore"))))
    z.close()
    return out


def read_any(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext in TEXT_EXT:
        with open(path, encoding="utf-8", errors="ignore") as f:
            return [("", f.read())]
    if ext in OOXML:
        return read_ooxml(path, ext)
    return []


def collect(target: str):
    if os.path.isfile(target):
        return [target]
    files = []
    for root, dirs, names in os.walk(target):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
        for n in sorted(names):
            if n.startswith("~$") or n.startswith("."):
                continue
            if os.path.splitext(n)[1].lower() in set(TEXT_EXT) | set(OOXML):
                files.append(os.path.join(root, n))
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="ファイルまたはフォルダ")
    ap.add_argument("--patterns", default=os.path.join(HERE, "patterns.json"))
    ap.add_argument("--add", action="append", default=[], help="プロジェクト固有の語を追加する")
    ap.add_argument("--quiet", action="store_true", help="ヒットのみ表示する")
    args = ap.parse_args()

    with open(args.patterns, encoding="utf-8") as f:
        groups = json.load(f)
    if args.add:
        groups["プロジェクト固有"] = args.add

    compiled = []
    for label, pats in groups.items():
        for p in pats:
            flags = re.M if p.startswith("^") else 0
            try:
                compiled.append((label, p, re.compile(p, flags)))
            except re.error:
                compiled.append((label, p, re.compile(re.escape(p), flags)))

    total = 0
    for path in collect(args.target):
        hits = []
        for section, text in read_any(path):
            for i, line in enumerate(text.splitlines(), start=1):
                s = line.strip()
                if not s:
                    continue
                for label, pat, rx in compiled:
                    if rx.search(line):
                        where = section or ("%d行目" % i)
                        hits.append((label, pat, where, s[:90]))
        if hits:
            total += len(hits)
            print("\n■ %s  （%d件）" % (os.path.relpath(path, os.getcwd()), len(hits)))
            for label, pat, where, s in hits:
                print("  [%s] %s  %s :: %s" % (label, pat, where, s))
        elif not args.quiet:
            print("  ok  %s" % os.path.relpath(path, os.getcwd()))

    print("\n合計 %d 件" % total)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
