# jp-client-deliverables

日本語の顧客提出物を作るためのスキル一式。要件定義フェーズのプロジェクトで受けた指摘を、
プロジェクトが終わっても持ち運べる形にまとめている。

固有名詞（発注元・元請け・製品名）は一般語に置き換えてある。実測値や語彙といった
プロジェクト固有の材料は `references/` 配下に「記入例」として残しており、次のプロジェクトでは
そこだけ差し替えれば使える。

## 収録スキル

| スキル | 担当範囲 |
|---|---|
| `japanese-business-writing` | 日本語の文章を書く。名詞化・体言止め・対比と因果連結・約束の強さ・語の統一・見出しとリード文・装飾と組版。納品前の機械走査つき |
| `japanese-rewrite` | すでにある下書きを、人が書いたと感じる日本語へ全面的に書き直す。口語で人らしさを装わない |
| `emphasis-first-drafting` | 書き始める前に重みの配分を確認。資料の濃淡を設計 |
| `deck-visual-design` | スライドの見せ方。配色・余白・罫線・文字サイズの段階。参照できる既存ページが無いときの初期値 |
| `pptx-house-style` | 顧客テンプレートに体裁を合わせる。実測 → 追従 → 機械検証。頻出トラブル6つの回避策。テンプレートのない新規デッキは HTML 先行・pptxgenjs 方式（10章） |
| `requirements-xlsx` | 要件定義Excelの書き方。記入ルールの宣言、採番規約、未決セルとコメント運用 |
| `deliverable-review-register` | 成果物を議事録と突き合わせ、修正案つきの指摘台帳にまとめる。要件書向けの品質チェックリストつき |
| `basic-design-review` | 基本設計を要件と双方向で照合し、記述の抜けと未決の確定化を洗い出す |
| `ai-design-prompt-review` | AI 向けの詳細設計とプロンプトを 10 項目で点検する。インジェクションへの備えを含む |
| `figure-construction` | スライドの主役になる図を 1 枚組み立てる。実企業スライド 40 枚の実測から出した組み立ての順序と形の寸法比 |
| `vibe-coding-evidence` | AI 駆動開発の主張を、普及・品質・保守性・攻撃側・確認側の 5 軸で外部データに当てて裏づける |

### 同梱スクリプト

いずれも `--help` で使い方が出る。

| スクリプト | 内容 | 依存 |
|---|---|---|
| `japanese-business-writing/scripts/scan_expressions.py` | md・pptx・xlsx・docx から本文を抽出。口語や記号の残りを走査 | 標準ライブラリのみ |
| `japanese-business-writing/scripts/ai_smell_score.py` | pptx・html・md・js の日本語を規則に当て、AI 臭さを 0〜100 で算出（10 未満で納品） | 標準ライブラリのみ（pptx は python-pptx） |
| `japanese-business-writing/scripts/scan_deck_jp.py` | 生成した pptx の日本語を抜き出し、実資料の実測の規則に当てる | python-pptx |
| `japanese-business-writing/scripts/check_html_data.js` | data.js の文言が HTML 版に含まれるかを突き合わせ（H-12） | Node.js |
| `pptx-house-style/scripts/pptx_measure.py` | 既存デッキの座標・級数・色・線幅を実測 | python-pptx, lxml |
| `pptx-house-style/scripts/fix_fonts.py` | theme / master / layout / slide の全レイヤーでフォントを統一 | 標準ライブラリのみ |
| `pptx-house-style/scripts/deckkit.py` | 罫線・テキスト枠・セル幅・見出し幅のヘルパ | python-pptx, lxml |
| `pptx-house-style/scripts/pptx_audit.py` | 文言差分・書式の一様性・フォント混在・はみ出しをチェック | python-pptx |
| `pptx-house-style/scripts/pptxgenjs/kit.js` | 1920×1080 px 座標の部品（DARK / LIGHT トークン、文字枠の高さ計算、表、リング） | pptxgenjs |
| `pptx-house-style/scripts/pptxgenjs/build_example.js` | kit.js の最小の使い方（`--light` でライト版） | pptxgenjs |
| `pptx-house-style/scripts/pptxgenjs/postprocess.py` | pptxgenjs の出力を全レイヤー 1 書体に統一し、typeface と級数をチェック | 標準ライブラリのみ |
| `pptx-house-style/scripts/pptxgenjs/html_overflow_check.js` | HTML 版の全枚を描画し、はみ出しと締めの帯との重なりを出力 | playwright |
| `pptx-house-style/scripts/pptxgenjs/html_to_png.js` | HTML の 1 要素を 2 倍解像度の PNG に変換（画像として貼る図だけ） | playwright |
| `pptx-house-style/scripts/contact_sheet.py` | 全ページを 1 枚に並べて目視 | Pillow |
| `requirements-xlsx/scripts/xlsx_open_items.py` | 未決セルとコメントを全件抽出。コメントの付いていない未決を警告 | 標準ライブラリのみ |
| `requirements-xlsx/scripts/xlsx_qa.py` | 提出前の Excel の静的チェック。数式エラー、外部リンク、非表示、名前定義、入力規則、シート間参照、表示形式の揺れ | openpyxl |
| `pptx-house-style/scripts/pptx_qa.py` | 提出前のスライドの静的チェック。文字切れ、フォント混在、重なり、ページ番号、タイトル重複、出典 | python-pptx |
| `pptx-house-style/scripts/pdf_qa.py` | PDF のページ数・構造・文字抽出可否をチェック | pypdf, qpdf |
| `*/scripts/qa_report.py` | チェック結果を JSON と Markdown で出力。両スキルに同じ内容を配置 | 標準ライブラリのみ |

## 導入

`.plugin` ファイルをチャットへ渡すか、リポジトリごと配置する。手順は `docs/getting-started-ja.md` にある。

## 次のプロジェクトで差し替える箇所

| ファイル | 差し替える内容 |
|---|---|
| `japanese-business-writing/references/phrase-table.md` | プロジェクトで指摘を受けた語を足す |
| `japanese-business-writing/scripts/patterns.json` | 上で追加した語を機械走査にも反映 |
| `pptx-house-style/references/measured-spec-example.md` | 対象デッキで測り直した値へ差し替える |
| `deck-visual-design/SKILL.md` のデザイントークン | `BASE` をテンプレートのブランド色へ |

## 使い分け

- 新規に資料を書く → `emphasis-first-drafting` で重みを決め、`japanese-business-writing` で書く
- 下書きが既にある → `japanese-rewrite`
- スライドを作る → 既存デッキがあれば `pptx-house-style`、無ければ `deck-visual-design`
- Excel定義書 → `requirements-xlsx`
- 他社の成果物を見る → `deliverable-review-register`
- 基本設計をレビューする → `basic-design-review`
- AI 向けの指示をレビューする → `ai-design-prompt-review`
- 図が主役のスライドを作る → `figure-construction`
- AI 駆動開発のリスクを根拠つきで説明する → `vibe-coding-evidence`

## ライセンス

MIT
