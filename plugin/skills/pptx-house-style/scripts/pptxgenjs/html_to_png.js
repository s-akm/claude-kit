// html_to_png.js — HTML の 1 要素を 2 倍解像度の PNG に書き出す（pptx に画像として貼る図だけに使う）。
//   node html_to_png.js deck.html 8 "#fig-p09" out/img_p09.png
//   引数: HTML、show() に渡す枚番号（0 始まり）、CSS セレクタ、出力先
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [file, idx, sel, out] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(file)); await p.evaluate(x => show(x), +idx); await p.waitForTimeout(150);
  const el = await p.$(sel); if (!el) { console.error('not found', sel); process.exit(2); }
  await el.screenshot({ path: out }); console.log('written', out);
  await b.close();
})();
