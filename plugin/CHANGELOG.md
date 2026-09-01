# 変更履歴

## 1.0.0 — 2026-09-01

要件定義フェーズの案件で蓄積した指摘を、案件から切り離してスキル化した初版。

- `japanese-business-writing` — 既存の日本語ビジネス文書スキルに、案件で受けた指摘19項目のうち
  未収録だった10項目を統合した（「同等」への統一、目的語を言い切る、列挙の括弧化、見出しの体言止め、
  中身のないリード文、隅付き括弧での範囲表示、造語の禁止、効果の誇張、二択に見せない、
  申し送り事項の根拠）。置換表を `references/phrase-table.md`、構成ルールを
  `references/document-structure.md` へ分離した。納品前の機械走査 `scan_expressions.py` を追加
- `japanese-rewrite` — 固有名詞を除去して移植
- `emphasis-first-drafting` — 質問ツールの記述を一般化して移植
- `deck-visual-design` — 顧客名を除去し、`pptx-house-style` との役割分担を明記して移植
- `pptx-house-style` — 顧客名を除去。本文中のコードを `scripts/` の4本へ切り出し、
  実測値の記入例を `references/measured-spec-example.md` に分離
- `requirements-xlsx` — 新規。要件定義Excelの記入ルール、採番規約、未決セルとコメント運用。
  `xlsx_open_items.py` で「コメントの付いていない未決セル」を検出する
- `deliverable-review-register` — 新規。議事録と成果物の双方向照合による指摘台帳の作り方。
  要件定義資料向けの4区分と、見積書向けの重要度S〜Dの2つの型を収録
