#!/usr/bin/env python3
"""要件定義Excelから、未決セルとコメントを全件抽出する。

「コメントの付いていない未決セル」を洗い出すのが目的。
標準ライブラリだけで動く（openpyxl は不要）。

    python3 xlsx_open_items.py 提出予定のフォルダ
    python3 xlsx_open_items.py 機能一覧.xlsx --grep "認証基盤"
    python3 xlsx_open_items.py . --pattern "要確認|要検討|TBD"
"""
import argparse
import os
import re
import sys
import zipfile

DEFAULT_PATTERN = r"要確認|要検討|確認中|未確定|未定|TBD|要相談|検討中|保留|要調整|\(要\)|（要）"
TAG = re.compile(r"<[^>]+>")


def strip_tags(x):
    x = re.sub(r"</a:p>|</w:p>|<br/>", "\n", x)
    return TAG.sub("", x).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").strip()


class Book:
    def __init__(self, path):
        self.path = path
        self.z = zipfile.ZipFile(path)
        self.names = self.z.namelist()
        self.shared = self._shared()
        self.sheets = self._sheets()

    def _read(self, n):
        return self.z.read(n).decode("utf-8", "ignore")

    def _shared(self):
        if "xl/sharedStrings.xml" not in self.names:
            return []
        raw = self._read("xl/sharedStrings.xml")
        return [strip_tags(m) for m in re.findall(r"<si>(.*?)</si>", raw, re.S)]

    def _sheets(self):
        """[(表示名, sheet xml path)] を workbook.xml の並び順で返す。"""
        out = []
        if "xl/workbook.xml" not in self.names:
            for n in sorted(x for x in self.names if re.match(r"xl/worksheets/sheet\d+\.xml$", x)):
                out.append((os.path.basename(n), n))
            return out
        wb = self._read("xl/workbook.xml")
        rels = {}
        if "xl/_rels/workbook.xml.rels" in self.names:
            for rid, tgt in re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"',
                                       self._read("xl/_rels/workbook.xml.rels")):
                rels[rid] = tgt if tgt.startswith("xl/") else "xl/" + tgt.lstrip("/")
        for m in re.finditer(r"<sheet\b[^>]*>", wb):
            tag = m.group(0)
            name = re.search(r'name="([^"]*)"', tag)
            rid = re.search(r'r:id="([^"]*)"', tag)
            target = rels.get(rid.group(1)) if rid else None
            if name and target and target in self.names:
                out.append((name.group(1), target))
        return out

    def cells(self, sheet_xml):
        """[(セル番地, 値)] を返す。"""
        raw = self._read(sheet_xml)
        res = []
        # 空セルは <c .../> と自己終端で書かれる。貪欲に拾うと次のセルを飲み込むため分けて扱う。
        for m in re.finditer(r"<c\b([^>]*?)(?:/>|>(.*?)</c>)", raw, re.S):
            attrs, inner = m.group(1), m.group(2) or ""
            ref = re.search(r'r="([A-Z]+\d+)"', attrs)
            if not ref:
                continue
            t = re.search(r't="([^"]+)"', attrs)
            t = t.group(1) if t else "n"
            if t == "s":
                v = re.search(r"<v>(\d+)</v>", inner)
                val = self.shared[int(v.group(1))] if v and int(v.group(1)) < len(self.shared) else ""
            elif t == "inlineStr":
                val = strip_tags(inner)
            else:
                v = re.search(r"<v>(.*?)</v>", inner, re.S)
                val = strip_tags(v.group(1)) if v else ""
            if val:
                res.append((ref.group(1), val))
        return res

    def comments(self, sheet_xml):
        """[(セル番地, 本文)] を返す。通常コメントとスレッドコメントの両方。"""
        base = os.path.basename(sheet_xml)
        relp = "xl/worksheets/_rels/%s.rels" % base
        targets = []
        if relp in self.names:
            for tgt in re.findall(r'Target="([^"]+)"', self._read(relp)):
                if "omment" in tgt:
                    targets.append(os.path.normpath(
                        os.path.join("xl/worksheets", tgt)).replace("\\", "/"))
        if not any("threadedComment" in t for t in targets):
            # threadedComments/threadedCommentN.xml は sheetN.xml と番号で対応する
            num = re.search(r"(\d+)", base)
            if num:
                cand = "xl/threadedComments/threadedComment%s.xml" % num.group(1)
                if cand in self.names:
                    targets.append(cand)
        out = []
        for t in targets:
            if t not in self.names:
                continue
            raw = self._read(t)
            if "threadedComment" in t:
                for m in re.finditer(
                        r'<threadedComment\b[^>]*ref="([A-Z]+\d+)"[^>]*>(.*?)</threadedComment>',
                        raw, re.S):
                    body = re.search(r"<text>(.*?)</text>", m.group(2), re.S)
                    out.append((m.group(1), strip_tags(body.group(1) if body else m.group(2))))
                continue
            for m in re.finditer(r'<comment\b[^>]*ref="([A-Z]+\d+)"[^>]*>(.*?)</comment>', raw, re.S):
                body = strip_tags(m.group(2))
                # スレッドコメントは comments1.xml 側に互換用の定型文が入る。実文は threadedComments 側。
                if "スレッド化されたコメント" in body:
                    continue
                out.append((m.group(1), body))
        return out


def collect(target):
    if os.path.isfile(target):
        return [target]
    files = []
    for root, dirs, names in os.walk(target):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for n in sorted(names):
            if n.lower().endswith(".xlsx") and not n.startswith("~$"):
                files.append(os.path.join(root, n))
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="ファイルまたはフォルダ")
    ap.add_argument("--pattern", default=DEFAULT_PATTERN, help="未決とみなす正規表現")
    ap.add_argument("--grep", help="この語を含むセルを横断検索する（資料間の整合確認用）")
    args = ap.parse_args()

    rx = re.compile(args.pattern)
    grep = re.compile(args.grep) if args.grep else None
    total_open, total_naked = 0, 0

    for path in collect(args.target):
        try:
            bk = Book(path)
        except Exception as e:
            print("■ %s  読めません: %s" % (path, e))
            continue
        rel = os.path.relpath(path, os.getcwd())
        open_rows, cmt_rows, grep_rows = [], [], []
        for name, xml in bk.sheets:
            cmap = dict(bk.comments(xml))
            for ref, val in bk.cells(xml):
                if grep and grep.search(val):
                    grep_rows.append((name, ref, val))
                if rx.search(val):
                    open_rows.append((name, ref, val, cmap.get(ref)))
            for ref, body in bk.comments(xml):
                cmt_rows.append((name, ref, body))

        if grep:
            if grep_rows:
                print("\n■ %s  「%s」を含むセル %d件" % (rel, args.grep, len(grep_rows)))
                for name, ref, val in grep_rows:
                    print("   %s!%s  %s" % (name, ref, val[:100]))
            continue

        naked = [r for r in open_rows if not r[3]]
        total_open += len(open_rows)
        total_naked += len(naked)
        print("\n■ %s" % rel)
        print("   未決セル %d件 / コメント %d件 / コメントなしの未決 %d件"
              % (len(open_rows), len(cmt_rows), len(naked)))
        for name, ref, val, cmt in open_rows:
            mark = "  " if cmt else "!!"
            print("   %s %s!%s  %s" % (mark, name, ref, val[:80]))
            if cmt:
                print("        └ %s" % cmt[:110])

    if not grep:
        print("\n未決 %d件、うちコメントなし %d件" % (total_open, total_naked))
        print("コメントなしの未決（!! 印）がゼロになるまで提出しない。")
    return 1 if total_naked else 0


if __name__ == "__main__":
    sys.exit(main())
