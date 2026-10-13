#!/usr/bin/env python3
"""pptxgenjs が書き出した pptx の後処理。

    python3 postprocess.py out/資料.pptx [--font 游ゴシック]

1. theme / slide の latin・ea・cs をすべて指定フォントに統一する（pptxgenjs は latin しか書かない run がある）
2. 使われている typeface と、級数の最小・最大を出す。typeface が 1 つでなければ終了コード 1
"""
import argparse, re, shutil, sys, zipfile

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('--font', default='游ゴシック')
a = ap.parse_args()
FONT, src, tmp = a.font, a.src, a.src + '.tmp'
zin = zipfile.ZipFile(src); zout = zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename.endswith('.xml'):
        s = data.decode('utf-8')
        if 'theme' in item.filename:
            for tag in ('latin', 'ea', 'cs'):
                s = re.sub(r'<a:%s typeface="[^"]*"' % tag, '<a:%s typeface="%s"' % (tag, FONT), s)
        if item.filename.startswith('ppt/slides/slide'):
            s = re.sub(r'<a:latin typeface="[^"]*"( [^>]*)?/>(?!<a:ea)',
                       lambda m: '<a:latin typeface="%s"%s/><a:ea typeface="%s"/><a:cs typeface="%s"/>' % (FONT, m.group(1) or '', FONT, FONT), s)
            for tag in ('latin', 'ea', 'cs'):
                s = re.sub(r'<a:%s typeface="[^"]*"' % tag, '<a:%s typeface="%s"' % (tag, FONT), s)
        data = s.encode('utf-8')
    zout.writestr(item, data)
zin.close(); zout.close(); shutil.move(tmp, src)

z = zipfile.ZipFile(src); faces = set(); sizes = []
for n in z.namelist():
    if n.startswith('ppt/slides/slide') and n.endswith('.xml'):
        s = z.read(n).decode()
        faces |= set(re.findall(r'typeface="([^"]*)"', s))
        sizes += [int(x) for x in re.findall(r'sz="(\d+)"', s)]
print('typefaces:', faces)
print('min pt: %.1f  max pt: %.1f' % (min(sizes) / 100, max(sizes) / 100))
sys.exit(0 if faces == {FONT} else 1)
