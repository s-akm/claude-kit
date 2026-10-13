// check_html_data.js — data.js の日本語文字列が HTML パーツに含まれるかを突き合わせる（H-12）。
// 使い方: node check_html_data.js pptx/data.js deck/00_head.html deck/01_part1.html ...
// 残るのは URL の改行と、タグで分かれた文字列だけになるまで直す。
const fs = require('fs'), path = require('path');
const [dataPath, ...htmlPaths] = process.argv.slice(2);
if (!dataPath || !htmlPaths.length) { console.error('usage: node check_html_data.js data.js part1.html ...'); process.exit(1); }
const D = require(path.resolve(dataPath));
const JP = /[぀-ヿ一-鿿]/;
const strs = [];
(function walk(v) { if (typeof v === 'string') { if (JP.test(v)) strs.push(v); } else if (Array.isArray(v)) v.forEach(walk); else if (v && typeof v === 'object') Object.values(v).forEach(walk); })(D);
const html = htmlPaths.map(p => fs.readFileSync(p, 'utf8')).join('').replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/\s+/g, '');
let miss = 0;
for (const s0 of strs) { const s = s0.replace(/\s+/g, ''); if (s.length < 6) continue; if (!html.includes(s)) { miss++; console.log(s0.slice(0, 100)); } }
console.log('data.js の文字列 ' + strs.length + ' 本 ／ HTML に見当たらないもの ' + miss + ' 本');
