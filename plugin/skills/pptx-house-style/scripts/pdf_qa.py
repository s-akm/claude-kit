#!/usr/bin/env python3
"""提出前の PDF を機械で検査する。元ファイルは変更しない。

    python3 pdf_qa.py 説明資料.pdf --out-dir 90_qa/2026-09-01-1200

検査する内容
    1. ページ数
    2. 構造の破損（qpdf --check。qpdf が無ければ pypdf の読み込み可否だけ）
    3. 文字を抽出できるか（ページごと）
    4. 暗号化・権限の設定
    5. ページサイズの揺れ

終了コード
    0 指摘なし / 1 警告あり / 2 提出できない指摘あり、またはファイルが読めない
"""
import argparse
import os
import shutil
import subprocess
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qa_report  # noqa: E402

MIN_CHARS = 20


def add(f, sev, check, where, what, how=""):
    f.append({"重要度": sev, "検査": check, "場所": where, "内容": what, "対応": how})


def check(path, min_chars=MIN_CHARS):
    from pypdf import PdfReader

    findings = []
    notes = []

    # --- 構造
    qpdf = shutil.which("qpdf")
    if qpdf:
        r = subprocess.run([qpdf, "--check", path], capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            head = (r.stdout + r.stderr).strip().splitlines()
            add(findings, "要確認", "構造破損", "ファイル全体",
                "qpdf --check が異常を返した: %s" % " / ".join(head[:3])[:200],
                "作り直すか、元のアプリから書き出し直す")
    else:
        notes.append("qpdf が入っていないため、構造の詳しい検査はしていない。"
                     "brew install qpdf で入る。")

    reader = PdfReader(path)

    if getattr(reader, "is_encrypted", False):
        add(findings, "警告", "暗号化", "ファイル全体",
            "暗号化されている", "提出先が開けるか確認する")

    pages = reader.pages
    total = len(pages)
    add(findings, "情報", "ページ数", "ファイル全体", "%d ページ" % total, "")

    sizes = Counter()
    empty = []
    for i, pg in enumerate(pages, start=1):
        try:
            box = pg.mediabox
            sizes[(round(float(box.width)), round(float(box.height)))] += 1
        except Exception:
            pass
        try:
            text = pg.extract_text() or ""
        except Exception:
            text = ""
        if len(text.strip()) < min_chars:
            empty.append(i)

    if empty:
        sev = "要確認" if len(empty) == total else "警告"
        add(findings, sev, "文字抽出", "ページ " + ",".join(map(str, empty[:20])),
            "文字を %d 字以上抽出できないページが %d / %d ある"
            % (min_chars, len(empty), total),
            "画像として貼られている可能性がある。検索と読み上げができない点を確認する")

    if len(sizes) > 1:
        add(findings, "警告", "ページサイズ", "ファイル全体",
            "ページサイズが %d 種類ある（%s）"
            % (len(sizes), " / ".join("%dx%d×%d枚" % (w, h, c) for (w, h), c in sizes.most_common(4))),
            "意図した混在か確認する")

    notes.append("見た目の崩れは判定していない。render-slides でページ画像を作って目視する。")
    return findings, notes


def main():
    ap = argparse.ArgumentParser(description="PDF の機械検査（元ファイルは変更しない）")
    ap.add_argument("file", help="検査する .pdf")
    ap.add_argument("--out-dir", default=".", help="結果の出力先")
    ap.add_argument("--stem", help="出力ファイル名（既定: pdf-<ファイル名>）")
    ap.add_argument("--min-chars", type=int, default=MIN_CHARS,
                    help="このページは文字が無いとみなす下限（既定 20）")
    args = ap.parse_args()

    if not os.path.isfile(args.file):
        print("ファイルがありません: %s" % args.file, file=sys.stderr)
        return 2

    versions = qa_report.tool_versions(["pypdf"])
    versions["qpdf"] = qa_report.cmd_version("qpdf")
    try:
        findings, notes = check(args.file, args.min_chars)
    except Exception as e:
        print("読めませんでした: %s: %s" % (type(e).__name__, e), file=sys.stderr)
        return 2

    report = qa_report.build("PDF", args.file, findings, versions, notes)
    stem = args.stem or ("pdf-" + os.path.splitext(os.path.basename(args.file))[0])
    jp, mp = qa_report.write(report, args.out_dir, stem)
    c = report["件数"]
    print("PDF    %s  要確認 %d / 警告 %d / 情報 %d  → %s"
          % (os.path.basename(args.file), c["要確認"], c["警告"], c["情報"], mp))
    return qa_report.exit_code(report)


if __name__ == "__main__":
    sys.exit(main())
