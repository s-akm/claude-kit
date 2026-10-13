// build_example.js — kit.js の最小の使い方。node build_example.js → out/example.pptx
//   1. data.js に文言を分離する（このファイルでは D にインライン）
//   2. 1 枚ごとに Kit.slideNo を進め、共通枠（kicker / h1 / 締めの帯 / footer）を frame() で置く
//   3. 書き出し後に postprocess.py でフォントを全レイヤー統一し、Kit.report() の件数を 0 にする
const pptxgen = require('pptxgenjs');
const path = require('path');
const { Kit, DARK, LIGHT } = require('./kit');

const THEME = process.argv.includes('--light') ? LIGHT : DARK;
const DECK = '資料名（フッター右）';
const D = {
  s01: { kicker: '第 1 章　見出しの上の小見出し', pg: '01', h1: '本文ページの見出し', conclusion: '締めの一文はここに置く', foot: '出典 〇〇「△△」2026 年',
    metrics: [
      { label: '指標 A', num: '84', unit: '%', ratio: .84, desc: '前年は 76%', src: '出典 A 2025' },
      { label: '指標 B', num: '25', unit: '%', ratio: .25, desc: '実測', src: '出典 B 2025' },
      { label: '指標 C', num: '46', unit: '%', ratio: .46, desc: '15 ポイント増', src: '出典 C 2025', hot: true },
    ] },
  s02: { kicker: '出典と用語', pg: '02', h1: '本資料で引いた数値の出どころ',
    head: ['項目', '出典', '参照ページ'],
    rows: [['指標 A', '出典 A「調査名」2025 年\nexample.com/report-a', 'P01'], ['指標 B', '出典 B 2025 年 3 月\nexample.com/report-b', 'P01']] },
};

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE'; pres.lang = 'ja-JP';
function newSlide() { const s = pres.addSlide(); s.background = { color: THEME.base }; Kit.slideNo += 1; return [s, Kit(pres, s, { T: THEME, deckTitle: DECK })]; }
function frame(k, d) { k.kicker(d.kicker, d.pg); k.h1(d.h1); if (d.conclusion) k.conclusion(d.conclusion); k.footer(d.foot || ''); }
const GAP = 32, colW = n => (1760 - GAP * (n - 1)) / n, colX = (i, n) => 80 + i * (colW(n) + GAP);

{ const [s, k] = newSlide(); const d = D.s01; frame(k, d);
  d.metrics.forEach((m, i) => k.metric(colX(i, 3), 224, colW(3), 440, m)); }

{ const [s, k] = newSlide(); const d = D.s02; frame(k, d);
  const rows = d.rows.map(([a, b, c]) => { const [nm, url] = b.split('\n'); return [a, url ? [{ t: nm + '\n', color: k.T.fg2 }, { t: url, color: k.T.fg3, px: url.length > 100 ? 10 : 11 }] : b, c]; });
  k.table(80, 224, 1760, [480, 1100, 180], d.head, rows, { rh: 66, px: 14.5, style: ci => ci === 0 ? { color: k.T.fg } : ci === 2 ? { color: k.T.fg3, px: 13 } : {} }); }

const out = path.join(__dirname, 'out', `example${THEME === LIGHT ? '_light' : ''}.pptx`);
require('fs').mkdirSync(path.dirname(out), { recursive: true });
pres.writeFile({ fileName: out }).then(() => { console.log('written', out); process.exitCode = Kit.report() ? 1 : 0; });
