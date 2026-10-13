# HTML 先行・pptxgenjs 方式の構成（記入例）

37 枚（本編 25＋章扉 6＋出典 1＋様式 5）の登壇資料を、HTML → pptx の順で作ったときの構成。
次に同じ方式で作るとき、フォルダをこの形に揃えれば `build.js` と検査がそのまま動く。

## フォルダ

```
deck-source/
  00_head.html          CSS（トークン・版面・部品）、← → 送りと N の設計メモ表示のスクリプト
  01_part1.html … 04_part4.html   本編の section。cat で 1 枚にする
  data.js               文言だけ。cover / s02 … s25 / chapters / sources / a1 … a5
  kit.js                トークン（DARK / LIGHT）と部品。scripts/pptxgenjs/kit.js をコピーして使う
  build.js              1 枚ずつ組む。newSlide() で Kit.slideNo を進め、frame() で共通枠を置く
  postprocess.py        フォント統一と typeface / 級数の検査
  rewrite.py            言い回し調整の置換一覧（見出し 19 本、語句 17 組）。data.js と HTML の両方に当てる
  update_data_2026.py   外部データを最新版へ差し替えたときの置換一覧
  img_p04.png / img_p09.png   HTML から 2 倍解像度で書き出した図（端末モック、模式図）
  README.md             再ビルド手順
```

## 再ビルド

```bash
cat 00_head.html 01_part1.html 02_part2.html 03_part3.html 04_part4.html > ../資料.html
node ../scripts/pptxgenjs/html_overflow_check.js ../資料.html          # はみ出し 0
node build.js                                                          # Kit.report() が 0
python3 postprocess.py "out/資料.pptx" --font 游ゴシック                # typeface が 1 つ
soffice --headless --convert-to pdf out/資料.pptx && pdftoppm -r 60 -png out/資料.pdf out/p
python3 ../scripts/pptx_qa.py out/資料.pptx --aft 0                    # 警告 0
python3 <japanese-business-writing>/scripts/scan_deck_jp.py out/資料.pptx
```

## 版面（1920×1080 px）

| 要素 | 位置・大きさ |
|---|---|
| kicker（章名・ページ番号） | y 64、15px、fg3 |
| h1 | y 104、h 80、54px 太字、行間 1.15 |
| 図の領域 | y 224 〜 940（締めの帯の 32px 上まで） |
| 締めの一文 | y 972、h 42、26px、左に brand の縦棒 3×30 |
| フッター罫線 / 脚注 / 資料名 | y 1024 / y 1034 12px fg3 / 右寄せ 12px |
| 左右の余白 | 80（本文幅 1760）。3 列なら列幅 (1760 − 32×2) / 3 |
| 章扉 | 版面の枠外。左に章番号 220px、右に章の 3 項目。進捗ドット 6 個を右上 |
| 数値カード | ラベル 12px 大文字 → 数字 96px＋単位 24px → 帯 6px → 説明 15px → 出典 12.5px（下揃え） |
| 出典表 | 列幅 480 / 1100 / 180、行高 66、本文 14.5px、URL 11px（100 字超は 10px） |

## 判断の記録（この資料で決めたこと）

- 画像にした図は 2 枚だけ（P04 端末モック＋DevTools、P09 模式図）。他の 35 枚は図形と文字
- ノートなし。発表原稿は `発表原稿.md`（敬体、各枚の目安秒数と累計、合計 20 分 50 秒）
- 出典の URL は出典一覧に併記（`https://` 省略）。一次資料が特定できない数値は資料から外した
- 外部データは発表日が決まった時点で最新版へ差し替える（`vibe-coding-evidence`）
- 「船舶保険の相互保険組合」のように伏せても特定されうる実績表現は、ユーザーの判断を取ってから使う
