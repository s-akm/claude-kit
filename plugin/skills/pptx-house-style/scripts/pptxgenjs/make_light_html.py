# make_light_html.py — Dark 版 HTML（結合済み）から Light 版 HTML を作る。
# kit.js の DARK→LIGHT の対応で、:root の変数・SVG の直書き色・半透明の色味を置き換える。
import re, sys
src, dst = sys.argv[1], sys.argv[2]
HEX = {  # DARK → LIGHT（kit.js と同じ役割名）
 '0A0A0B': 'FFFFFF', '141417': 'F7F7F8', '1C1C21': 'EDEDF0', '2A2A31': 'E1E1E6', '3F3F49': 'C9C9D1',
 'F4F4F5': '18181B', 'A1A1AA': '52525B', '63636B': '8A8A94', '6E7CFF': '4F5BD5', '22C55E': '15803D', 'FF4D5E': 'D93648', 'F5A524': 'B7791F',
 '8FA3FF': '4F5BD5',                       # 表紙の端末画面のキー名
 '0F0F12': 'F7F7F8', '17171B': 'E1E1E6',   # P04 の端末モックの地と縁
 '0C0C0F': 'F7F7F8',                       # ノート欄の地
}
RGB = {  # 半透明の色味（brand / danger / ok / warn）
 '110,124,255': '79,91,213', '255,77,94': '217,54,72', '34,197,94': '21,128,61', '245,165,36': '183,121,31',
}
s = open(src, encoding='utf-8').read()
n = 0
for a, b in HEX.items():
    c = len(re.findall('#' + a, s, flags=re.I)); n += c
    s = re.sub('#' + a, '#' + b, s, flags=re.I)
for a, b in RGB.items():
    c = s.count('rgba(' + a); n += c
    s = s.replace('rgba(' + a, 'rgba(' + b)
s = s.replace('rgba(0,0,0,.7)', 'rgba(0,0,0,.15)')  # 端末モックの影
s = s.replace('.seg.ver{background:rgba(217,54,72,.35)', '.seg.ver{background:rgba(217,54,72,.28)')
open(dst, 'w', encoding='utf-8').write(s)
left = sorted(set(re.findall(r'#([0-9A-Fa-f]{6})\b', s)))
print('replaced', n, 'remaining hex', left)
