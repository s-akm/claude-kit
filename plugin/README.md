# jp-client-deliverables

日本語の顧客提出物を作るためのスキル一式。要件定義フェーズの実案件で受けた指摘を、
案件が終わっても持ち運べる形にまとめている。

固有名詞（発注元・元請け・製品名）は一般語に置き換えてある。実測値や語彙といった
案件固有の材料は `references/` 配下に「記入例」として残しており、次の案件では
そこだけ差し替えれば使える。

## 収録スキル

| スキル | 担当範囲 |
|---|---|
| `japanese-business-writing` | 日本語の文章を書く。名詞化・体言止め・約束の強さ・語の統一・見出しとリード文・組版。納品前の機械走査つき |
| `japanese-rewrite` | すでにある下書きを、人が書いたと感じる日本語へ全面的に書き直す |
| `emphasis-first-drafting` | 書き始める前に「どこに重きを置くか」を確認し、資料の濃淡を設計する |
| `deck-visual-design` | スライドの見せ方。配色・余白・罫線・文字サイズの段階。参照できる既存ページが無いときの初期値 |
| `pptx-house-style` | 顧客テンプレートに体裁を合わせる。実測 → 追従 → 機械検証。頻出トラブル6つの回避策 |
| `requirements-xlsx` | 要件定義Excelの書き方。記入ルールの宣言、採番規約、未決セルとコメント運用 |
| `deliverable-review-register` | 成果物を議事録と突き合わせ、修正案つきの指摘台帳にまとめる |

### 同梱スクリプト

いずれも `--help` で使い方が出る。

| スクリプト | 内容 | 依存 |
|---|---|---|
| `japanese-business-writing/scripts/scan_expressions.py` | md・pptx・xlsx・docx から本文を取り出し、口語や記号の残りを走査する | 標準ライブラリのみ |
| `pptx-house-style/scripts/pptx_measure.py` | 既存デッキの座標・級数・色・線幅を実測する | python-pptx, lxml |
| `pptx-house-style/scripts/fix_fonts.py` | theme / master / layout / slide の全レイヤーでフォントを統一する | 標準ライブラリのみ |
| `pptx-house-style/scripts/deckkit.py` | 罫線・テキスト枠・セル幅・見出し幅のヘルパ | python-pptx, lxml |
| `pptx-house-style/scripts/pptx_audit.py` | 文言差分・書式の一様性・フォント混在・はみ出しを検査する | python-pptx |
| `pptx-house-style/scripts/contact_sheet.py` | 全ページを1枚に並べて目視する | Pillow |
| `requirements-xlsx/scripts/xlsx_open_items.py` | 未決セルとコメントを全件抽出し、コメントの付いていない未決を警告する | 標準ライブラリのみ |
| `requirements-xlsx/scripts/xlsx_qa.py` | 提出前の Excel を検査する。数式エラー、外部リンク、非表示、名前定義、入力規則、シート間参照、表示形式の揺れ | openpyxl |
| `pptx-house-style/scripts/pptx_qa.py` | 提出前のスライドを検査する。文字切れ、フォント混在、重なり、ページ番号、タイトル重複、出典 | python-pptx |
| `pptx-house-style/scripts/pdf_qa.py` | PDF のページ数・構造・文字抽出可否を検査する | pypdf, qpdf |
| `*/scripts/qa_report.py` | 検査結果を JSON と Markdown で書き出す。両スキルに同じ内容を置いている | 標準ライブラリのみ |

## 導入

`.plugin` ファイルをチャットへ渡すか、リポジトリごと配置する。手順は `docs/導入手順.md` にある。

## 次の案件で差し替える箇所

| ファイル | 差し替える内容 |
|---|---|
| `japanese-business-writing/references/phrase-table.md` | 案件で指摘を受けた語を足す |
| `japanese-business-writing/scripts/patterns.json` | 上で足した語を機械走査にも反映する |
| `pptx-house-style/references/measured-spec-example.md` | 対象デッキで測り直した値へ差し替える |
| `deck-visual-design/SKILL.md` のデザイントークン | `BASE` をテンプレートのブランド色へ |

## 使い分け

- 新規に資料を書く → `emphasis-first-drafting` で重みを決め、`japanese-business-writing` で書く
- 下書きが既にある → `japanese-rewrite`
- スライドを作る → 既存デッキがあれば `pptx-house-style`、無ければ `deck-visual-design`
- Excel定義書 → `requirements-xlsx`
- 他社の成果物を見る → `deliverable-review-register`

## ライセンス

MIT
