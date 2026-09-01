#!/usr/bin/env python3
"""全ページを1枚に並べたコンタクトシートを作る。

行数の偏り、スカスカのページ、1行しかない表のページが一目で分かる。

    soffice --headless --convert-to pdf deck.pptx --outdir .
    pdftoppm -r 90 -jpeg deck.pdf page
    python3 contact_sheet.py 'page-*.jpg' -o contact.jpg
"""
import argparse
import glob

from PIL import Image


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pattern", nargs="?", default="page-*.jpg")
    ap.add_argument("-o", "--out", default="contact.jpg")
    ap.add_argument("--cols", type=int, default=4)
    args = ap.parse_args()

    files = sorted(glob.glob(args.pattern))
    if not files:
        print("画像が見つかりません: %s" % args.pattern)
        return
    ims = [Image.open(f) for f in files]
    w, h = ims[0].size
    rows = (len(ims) + args.cols - 1) // args.cols
    sheet = Image.new("RGB", (w // 2 * args.cols, h // 2 * rows), "white")
    for i, im in enumerate(ims):
        sheet.paste(im.resize((w // 2, h // 2)),
                    ((i % args.cols) * (w // 2), (i // args.cols) * (h // 2)))
    sheet.save(args.out, quality=84)
    print("%s（%dページ）" % (args.out, len(ims)))


if __name__ == "__main__":
    main()
