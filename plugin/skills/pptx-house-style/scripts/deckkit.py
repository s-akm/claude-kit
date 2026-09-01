#!/usr/bin/env python3
"""体裁ヘルパ。頻出トラブルを踏まないための最小セット。

python-pptx の既定挙動が原因で起きる事故を回避する。
生成スクリプトから import して使う。

    from deckkit import body, rule, visible_line, fits, fix_circled
"""
from lxml import etree

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
AN = "{%s}" % A
IN = 914400
CIRC = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳"
_uid = [9000]


def body(sh, anchor="t"):
    """(a) テキスト枠の設定差による位置ズレを潰す。揃えたい枠すべてに適用する。"""
    bp = sh.text_frame._txBody.find(AN + "bodyPr")
    for t in ("spAutoFit", "normAutofit", "noAutofit"):
        for e in bp.findall(AN + t):
            bp.remove(e)
    bp.set("anchor", anchor)
    for k in ("lIns", "tIns", "rIns", "bIns"):
        bp.set(k, "0")
    bp.set("wrap", "square")
    return sh


def rule(slide, x, y, w, col="DCE3EA", wid=6350):
    """(b) 影の乗らない罫線を生XMLで引く。wid: 6350=0.5pt / 12700=1.0pt"""
    _uid[0] += 1
    xml = ('<p:sp xmlns:p="%s" xmlns:a="%s">'
           '<p:nvSpPr><p:cNvPr id="%d" name="rule%d"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
           '<p:spPr><a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="0"/></a:xfrm>'
           '<a:prstGeom prst="line"><a:avLst/></a:prstGeom>'
           '<a:ln w="%d"><a:solidFill><a:srgbClr val="%s"/></a:solidFill></a:ln></p:spPr>'
           '<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr/></a:p></p:txBody></p:sp>'
           ) % (P, A, _uid[0], _uid[0], int(x * IN), int(y * IN), int(w * IN), wid, col)
    slide.shapes._spTree.append(etree.fromstring(xml))


def visible_line(sh):
    """(c) noFill の線に solidFill を足さないよう、可視の線だけを返す。"""
    try:
        return sh.line.color if sh.line.fill.type == 1 else None
    except Exception:
        return None


def est_height_in(sh, lnpct=1.40, aft_pt=3):
    """(d) 推定描画高さ（インチ）。全角=1em、半角=0.55em で行数を見積もる。"""
    w = sh.width / IN * 72.0 - 4
    tot = 0.0
    for p in sh.text_frame.paragraphs:
        if not p.text.strip():
            tot += 6
            continue
        sz = max([r.font.size.pt for r in p.runs if r.font.size] or [10.5])
        em = sum(1.0 if ord(c) > 0x2000 else 0.55 for c in p.text) * sz
        tot += max(1, int(em / w) + 1) * sz * lnpct + aft_pt
    return tot / 72.0


def cell_min_width_in(text, pt=7.5, margin_in=0.19):
    """(e) 付加記号まで含めたセルの最低幅。区分列・ステータス列で必ず使う。"""
    em = sum(1.0 if ord(c) > 0x2000 else 0.55 for c in text)
    return em * pt / 72.0 + margin_in


def fits(text, width_in, pt=13.5):
    """(f) 見出しが枠幅に収まるか。False なら枠を広げず語を削る。"""
    em = sum(1.0 if ord(c) > 0x2000 else 0.55 for c in text)
    return em * pt / 72.0 <= width_in


def fix_circled(tf):
    """段落先頭の丸付き数字だけを 1. 2. 3. へ置換する。固有名詞中のものは残す。"""
    for p in tf.paragraphs:
        if not p.runs:
            continue
        t = p.text
        if not t or t[0] not in CIRC:
            continue
        r0 = p.runs[0]
        if r0.text and r0.text[0] in CIRC:
            r0.text = "%d." % (CIRC.index(t[0]) + 1) + r0.text[1:]
