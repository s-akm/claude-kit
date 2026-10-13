// html_overflow_check.js — HTML 版の全枚を 1920×1080 で描画し、版面からのはみ出しと、図と締めの帯の重なりを出す。
//   node html_overflow_check.js deck.html [--shots out_dir]
// 前提: HTML 側に window.slides（section の配列）と show(i) があり、表示中の section に .active が付く。
//       締めの帯は .conclusion、図の領域は .panels。
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = path.resolve(process.argv[2]);
  const si = process.argv.indexOf('--shots'); const shots = si > 0 ? process.argv[si + 1] : null;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + file);
  const n = await p.evaluate(() => slides.length);
  const issues = await p.evaluate(() => {
    const out = [];
    slides.forEach(s => {
      s.classList.add('active');
      s.querySelectorAll('*').forEach(el => { const r = el.getBoundingClientRect();
        if (r.width > 0 && (r.right > 1921 || r.bottom > 1081)) out.push(`${s.dataset.n || ''} overflow ${el.tagName}.${el.className} ${Math.round(r.right)}x${Math.round(r.bottom)}`); });
      const pn = s.querySelector('.panels'), cc = s.querySelector('.conclusion');
      if (pn && cc) { const a = pn.getBoundingClientRect(), c = cc.getBoundingClientRect();
        if (a.bottom > c.top - 10) out.push(`${s.dataset.n || ''} panels reach conclusion ${Math.round(a.bottom)}>${Math.round(c.top)}`); }
      s.classList.remove('active');
    });
    return out;
  });
  console.log('slides', n); console.log(issues.length ? issues.join('\n') : 'no overflow');
  if (shots) { require('fs').mkdirSync(shots, { recursive: true });
    for (let i = 0; i < n; i++) { await p.evaluate(x => show(x), i); await p.waitForTimeout(80); await p.screenshot({ path: path.join(shots, `s${String(i + 1).padStart(2, '0')}.png`) }); } }
  await b.close(); process.exitCode = issues.length ? 1 : 0;
})();
