// kit.js — pptxgenjs で 1920×1080 の px 座標から pptx を組む部品。
//
//   const { Kit, DARK, LIGHT, pt, inch } = require('./kit');
//   const k = Kit(pres, slide, { T: DARK, font: '游ゴシック', deckTitle: '資料名' });
//
// 座標・幅・高さ・級数はすべて HTML と同じ px で受け取り、内部で inch / pt に変換する。
//   1920px = 13.333in → 1px = 1/144in、px × 0.5 = pt（8pt 未満は 8pt に切り上げ）
// 文字枠の高さは h を 'auto' にすると 行数 × 級数 × 行間 で計算する。数値で渡した場合も
// 必要な高さと比べ、足りなければ Kit.warnings に積む（build の最後に Kit.report() で件数を出す）。

const DARK = {
  base: '0A0A0B', surface: '141417', elev: '1C1C21', border: '2A2A31', borderS: '3F3F49',
  fg: 'F4F4F5', fg2: 'A1A1AA', fg3: '63636B', brand: '6E7CFF', ok: '22C55E', danger: 'FF4D5E', warn: 'F5A524',
  // 半透明の地は透明度でなく、base に混色した実色で持つ（透明度は枠線と PDF 変換で崩れる）
  brandBg: '1A1D30', dangerBg: '2A1418', okBg: '112418', warnBg: '2A2114',
  brandLine: '3F4784', dangerLine: '8A2E38', okLine: '1E6B3F', warnLine: '86602A',
  dangerFill: '5C1F27',  // 警告の帯（danger を 35% 混色）。塗りで強調する箇所だけに使う
  termKey: '8FA3FF',     // 表紙の端末画面のキー名（brand を明るくした色）
  chapterNum: '3A3A40',  // 章扉の特大番号（base に近い無彩色）
  minusPanel: '181214',  // 差分表示の「要望のまま」側の地（dangerBg より薄い）
  plusPanel: '131420',   // 差分表示の「受け入れ条件」側の地（brandBg より薄い）
};
// ライト版の初期値。base 白地に対して同じ役割名で持つ（deck-visual-design の 2 色構成に寄せる）
const LIGHT = {
  base: 'FFFFFF', surface: 'F7F7F8', elev: 'EDEDF0', border: 'E1E1E6', borderS: 'C9C9D1',
  fg: '18181B', fg2: '52525B', fg3: '8A8A94', brand: '4F5BD5', ok: '15803D', danger: 'D93648', warn: 'B7791F',
  brandBg: 'EEF0FF', dangerBg: 'FDECEE', okBg: 'E9F7EE', warnBg: 'FBF3E4',
  brandLine: 'B9C0F5', dangerLine: 'F2B4BC', okLine: 'A9DDBB', warnLine: 'EAD3A3',
  dangerFill: 'F6C3C9',
  termKey: '4F5BD5', chapterNum: 'DCDCE2', minusPanel: 'FDF5F6', plusPanel: 'F3F4FC',
};

const PX = 1 / 144;
const pt = px => Math.max(8, Math.round(px * 0.5 * 2) / 2);
const inch = px => +(px * PX).toFixed(4);
// 級数を pt に丸めた後の実効 px（8pt 切り上げがあるため、元の px より大きくなることがある）
const effPx = px => pt(px) * 2;
// 文字幅の見積もり（px）。ASCII 0.55em、それ以外 1em。実測より広めに出るので枠は余る側に倒れる
const textW = (s, px) => [...String(s)].reduce((a, ch) => a + (/[\x00-\x7F]/.test(ch) ? 0.55 : 1.0) * effPx(px), 0);

function Kit(pres, slide, opt = {}) {
  const T = opt.T || DARK;
  const FONT = opt.font || '游ゴシック';
  const DECK = opt.deckTitle || '';
  const k = { T, FONT };

  k.rect = (x, y, w, h, o = {}) => {
    const p = { x: inch(x), y: inch(y), w: inch(w), h: inch(h),
      fill: o.fill ? { color: o.fill } : { type: 'none' },
      line: o.line ? { color: o.line, width: o.lw || 0.75 } : { type: 'none' } };
    if (o.dash) p.line.dashType = o.dash;
    if (o.r) { p.rectRadius = inch(o.r); slide.addShape(pres.shapes.ROUNDED_RECTANGLE, p); }
    else slide.addShape(pres.shapes.RECTANGLE, p);
  };
  k.line = (x1, y1, x2, y2, o = {}) => slide.addShape(pres.shapes.LINE, {
    x: inch(x1), y: inch(y1), w: inch(x2 - x1), h: inch(y2 - y1),
    line: { color: o.color || T.border, width: o.lw || 0.75, dashType: o.dash || 'solid' } });
  k.vbar = (x, y, h, color, w = 3) => k.rect(x, y, w, h, { fill: color, r: 1.5 });
  k.ellipse = (x, y, w, h, o = {}) => slide.addShape(pres.shapes.OVAL, {
    x: inch(x), y: inch(y), w: inch(w), h: inch(h),
    fill: o.fill ? { color: o.fill } : { type: 'none' }, line: o.line ? { color: o.line, width: o.lw || 0.75 } : { type: 'none' } });
  k.dot = (x, y, color, d = 8) => k.ellipse(x, y, d, d, { fill: color });
  // 円弧のリング（割合表示）。pptxgenjs の ARC は 90° を越えると崩れることがあるため、90° ずつに割る
  k.ring = (cx, cy, r, ratio, o = {}) => {
    const lw = o.lw || 13;
    k.ellipse(cx - r, cy - r, 2 * r, 2 * r, { line: o.track || T.elev, lw });
    let start = 270, rest = 360 * ratio;
    while (rest > 0) {
      const span = Math.min(90, rest); const end = (start + span) % 360;
      slide.addShape(pres.shapes.ARC, { x: inch(cx - r), y: inch(cy - r), w: inch(2 * r), h: inch(2 * r),
        angleRange: [start, end === 0 ? 360 : end], line: { color: o.color || T.danger, width: lw } });
      start = end; rest -= span;
    }
  };

  // 文字枠。str は文字列か runs [{t, color, bold, px, breakLine}]。
  //   h に 'auto' を渡すと必要な高さで作る。数値を渡した場合は必要な高さと比べて警告を積む。
  k.textNeed = (str, w, o = {}) => {
    const runs = Array.isArray(str) ? str : [{ t: String(str) }];
    const basePx = o.px || 15.5, lh = o.lh || 1.35;
    let lines = 0, maxPx = 0;
    const paras = [];
    let cur = [];
    runs.forEach(r => { cur.push(r); if (r.breakLine) { paras.push(cur); cur = []; } });
    if (cur.length) paras.push(cur);
    paras.forEach(pr => {
      const text = pr.map(r => r.t).join('');
      text.split('\n').forEach(seg => {
        const segRuns = pr.length === 1 ? [{ t: seg, px: pr[0].px }] : pr;
        const width = segRuns.reduce((a, r) => a + textW(r.t, r.px || basePx), 0);
        const px = Math.max(...segRuns.map(r => effPx(r.px || basePx)));
        maxPx = Math.max(maxPx, px);
        lines += o.wrap === false ? 1 : Math.max(1, Math.ceil(width / Math.max(1, w - 8)));  // pptx_qa.py と同じく左右 4pt を差し引く
      });
    });
    return Math.ceil(lines * maxPx * lh + (o.paraSpaceAfter || 0) * 2 * Math.max(0, paras.length - 1));
  };
  k.text = (x, y, w, h, str, o = {}) => {
    const size = pt(o.px || 15.5);
    const need = k.textNeed(str, w, o);
    if (h === 'auto' || h == null) h = need;
    else if (need > h * 1.02) Kit.warnings.push({ slide: Kit.slideNo, text: (Array.isArray(str) ? str.map(r => r.t).join('') : String(str)).slice(0, 24), h, need });
    const base = { fontFace: FONT, fontSize: size, color: o.color || T.fg, bold: !!o.bold };
    const runs = Array.isArray(str)
      ? str.map(r => ({ text: r.t, options: { ...base, ...(r.color ? { color: r.color } : {}), ...(r.bold != null ? { bold: r.bold } : {}), ...(r.px ? { fontSize: pt(r.px) } : {}), ...(r.breakLine ? { breakLine: true } : {}) } }))
      : [{ text: String(str), options: base }];
    slide.addText(runs, { x: inch(x), y: inch(y), w: inch(w), h: inch(h), isTextBox: true, margin: 0,
      align: o.align || 'left', valign: o.valign || 'top', fontFace: FONT, fontSize: size, color: o.color || T.fg,
      lineSpacingMultiple: o.lh || 1.35, charSpacing: o.cs || 0, fit: 'none', wrap: o.wrap !== false,
      ...(o.paraSpaceAfter ? { paraSpaceAfter: o.paraSpaceAfter } : {}) });
    return h;
  };
  k.textW = textW;
  k.image = (path, x, y, w, h) => slide.addImage({ path, x: inch(x), y: inch(y), w: inch(w), h: inch(h) });

  // ---- 版面の共通枠（上 64 / 左右 80 / 下 28。締めの帯は全ページ同じ y）----
  k.kicker = (left, pg) => {
    k.text(80, 64, 1400, 'auto', left, { px: 19, color: T.fg3 });
    if (pg) k.text(1640, 64, 200, 'auto', pg, { px: 19, color: T.fg3, align: 'right' });
  };
  k.h1 = (runs) => k.text(80, 104, 1760, 80, runs, { px: 54, bold: true, lh: 1.15, valign: 'middle' });
  k.conclusion = (s) => { k.vbar(80, 978, 30, T.brand); k.text(102, 972, 1700, 42, s, { px: 26, valign: 'middle' }); };
  k.footer = (left, right = DECK) => {
    k.line(80, 1024, 1840, 1024, { color: T.border });
    if (left) k.text(80, 1034, right ? 1330 : 1760, 'auto', left, { px: 16, color: T.fg3, lh: 1.2 });  // 資料名を置かないときは脚注を全幅に（1 行に収める）
    if (right) k.text(1440, 1034, 400, 'auto', right, { px: 16, color: T.fg3, align: 'right' });
  };
  k.label = (x, y, w, s, color = T.fg3) => k.text(x, y, w, 'auto', String(s).toUpperCase(), { px: 16, bold: true, color, cs: 1.2 });
  k.panel = (x, y, w, h, o = {}) => k.rect(x, y, w, h, { fill: o.fill || T.surface, line: o.line || T.border, r: o.r == null ? 16 : o.r, lw: o.lw });

  // タグ。幅は文字幅の見積もり＋左右 15px。横に並べるときは戻り値の幅で次の x を決める
  k.tag = (x, y, s, kind = 'ghost', o = {}) => {
    const w = o.w || Math.round(textW(s, 12) + 30);
    const map = { ghost: [null, T.border, T.fg3], brand: [T.brandBg, T.brandLine, T.brand], danger: [T.dangerBg, T.dangerLine, T.danger],
      dangerLine: [null, T.dangerLine, T.danger], ok: [T.okBg, T.okLine, T.ok], warn: [T.warnBg, T.warnLine, T.warn], fg: [T.elev, T.border, T.fg2] };
    const [fill, line, color] = map[kind];
    k.rect(x, y, w, 32, { fill, line, r: 6 });
    k.text(x, y, w, 32, s, { px: 16, color, align: 'center', valign: 'middle', bold: !!o.bold, wrap: false });
    return w;
  };
  k.nbadge = (x, y, s, kind = 'brand') => {
    const map = { brand: [T.brandBg, T.brandLine, T.brand], danger: [T.dangerBg, T.dangerLine, T.danger], fg: [T.elev, T.border, T.fg2] };
    const [fill, line, color] = map[kind];
    k.rect(x, y, 44, 30, { fill, line, r: 6 });
    k.text(x, y, 44, 30, s, { px: 16, color, bold: true, align: 'center', valign: 'middle', wrap: false });
  };
  k.meter = (x, y, w, ratio, color = T.brand, h = 6) => {
    k.rect(x, y, w, h, { fill: T.elev, r: h / 2 });
    if (ratio > 0) k.rect(x, y, Math.max(h, w * ratio), h, { fill: color, r: h / 2 });
  };
  // 見出し＋横の副見出し。副見出しの x は見出しの文字幅から決め、枠を重ねない
  k.headline = (x, y, w, h, sub, o = {}) => {
    const px = o.px || 22, hw = Math.min(w, Math.ceil(textW(h, px)) + 16);
    k.text(x, y, hw, 'auto', h, { px, bold: true });
    if (sub) k.text(x + hw + 12, y + Math.round(effPx(px) * 0.35), w - hw - 12, 'auto', sub, { px: o.subPx || 13, color: T.fg3 });
  };
  // 数値カード（ラベル／特大の数字＋単位／帯／説明／出典）
  k.metric = (x, y, w, h, m) => {
    const hot = !!m.hot;
    k.panel(x, y, w, h, { line: hot ? T.dangerLine : T.border });
    k.label(x + 32, y + 30, w - 64, m.label);
    const numPx = m.numPx || 96;
    k.text(x + 30, y + 64, w - 60, numPx * 1.15, [{ t: m.num, color: hot ? T.danger : T.fg, bold: true, px: numPx }, { t: '  ' + (m.unit || ''), color: T.fg2, px: 24 }], { px: numPx, lh: 1.0, valign: 'bottom', wrap: false });
    let cy = y + 64 + numPx * 1.15 + 20;
    if (m.ratio != null) { k.meter(x + 32, cy, w - 64, m.ratio, hot ? T.danger : T.brand); cy += 22; }
    if (m.desc) k.text(x + 32, cy, w - 64, 'auto', m.desc, { px: 19, color: T.fg2, lh: 1.5 });
    if (m.src) k.text(x + 32, y + h - 76, w - 64, 56, m.src, { px: 16, color: T.fg3, lh: 1.4, valign: 'bottom' });
  };
  // 表。列幅 cols[]、行高 rh。セルは文字列か runs。style(ci, ri) で列ごとの色・級数
  k.table = (x, y, w, cols, head, rows, o = {}) => {
    const rh = o.rh || 66, hh = o.hh || 48, px = o.px || 14.5, pad = o.pad == null ? 10 : o.pad, lh = o.lh || 1.3;
    k.panel(x, y, w, hh + rows.length * rh, { r: 12 });
    k.rect(x, y, w, hh, { fill: T.elev, r: 12 }); k.rect(x, y + hh - 12, w, 12, { fill: T.elev });
    let cx = x; head.forEach((hd, ci) => { k.text(cx + 22, y, cols[ci] - 44, hh, hd, { px: 16, bold: true, color: T.fg2, valign: 'middle', cs: 1 }); cx += cols[ci]; });
    rows.forEach((row, ri) => {
      const ry = y + hh + ri * rh; if (ri) k.line(x, ry, x + w, ry);
      let cx2 = x;
      row.forEach((cell, ci) => { k.text(cx2 + 22, ry + pad, cols[ci] - 44, rh - pad * 2, cell, { px, color: T.fg2, lh, valign: 'top', ...(o.style ? o.style(ci, ri) : {}) }); cx2 += cols[ci]; });
    });
    return y + hh + rows.length * rh;
  };
  return k;
}
Kit.warnings = [];
Kit.slideNo = 0;
Kit.report = () => {
  if (!Kit.warnings.length) { console.log('text boxes: all fit'); return 0; }
  Kit.warnings.forEach(w => console.log(`slide ${w.slide}: box ${w.h}px < need ${w.need}px 「${w.text}」`));
  console.log(`text boxes too small: ${Kit.warnings.length}`);
  return Kit.warnings.length;
};
module.exports = { Kit, DARK, LIGHT, pt, inch, effPx, textW };
