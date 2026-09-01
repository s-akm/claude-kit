#!/usr/bin/env python3
"""フォントを全レイヤー（theme / slideMaster / slideLayout / slide）で統一する。

展開済みの ppt ディレクトリを対象にする。XMLを書き出すたびに毎回流す。

    unzip -q deck.pptx -d work
    python3 fix_fonts.py work/ppt --font 游ゴシック
    cd work && zip -qr ../deck_fixed.pptx .
"""
import argparse
import glob
import io
import os
import re


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ppt_dir", help="展開済みの ppt ディレクトリ")
    ap.add_argument("--font", default="游ゴシック")
    args = ap.parse_args()
    f = args.font
    d = args.ppt_dir

    for path in glob.glob(os.path.join(d, "theme", "theme*.xml")):
        s = io.open(path, encoding="utf-8").read()
        s = re.sub(r'(<a:(?:major|minor)Font>\s*<a:latin typeface=")[^"]*(")',
                   r"\g<1>" + f + r"\g<2>", s)
        s = re.sub(r'(<a:(?:major|minor)Font>\s*<a:latin[^>]*/>\s*<a:ea typeface=")[^"]*(")',
                   r"\g<1>" + f + r"\g<2>", s)
        io.open(path, "w", encoding="utf-8").write(s)

    targets = (glob.glob(os.path.join(d, "slideMasters", "*.xml"))
               + glob.glob(os.path.join(d, "slideLayouts", "*.xml"))
               + glob.glob(os.path.join(d, "slides", "*.xml")))
    for path in targets:
        s = io.open(path, encoding="utf-8").read()
        s = re.sub(r'(<a:(?:latin|ea|cs) typeface=")(?!\+)[^"]*(")', r"\g<1>" + f + r"\g<2>", s)
        s = s.replace('typeface=""', 'typeface="%s"' % f)
        io.open(path, "w", encoding="utf-8").write(s)

    print("%s を %d ファイルへ適用しました" % (f, len(targets) + 1))


if __name__ == "__main__":
    main()
