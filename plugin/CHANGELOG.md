# 変更履歴

## 1.2.0 — 2026-09-01

レビュー側のスキルを 2 件足し、要件書向けのチェックリストを追加した。スキルは 7 件から 9 件になった。

- `basic-design-review` — 新規。要件側と設計側の双方向照合、記述の欠落（画面・API・データ・権限・
  エラー処理・バッチ）、非機能 6 区分、運用と保守と障害対応、未決の確定化、用語と識別子と数値と
  図表の整合。観点表と良い例・悪い例を `references/` に置いた
- `ai-design-prompt-review` — 新規。AI 向けの指示を 10 項目で点検する。書いていないことと
  書きすぎの両方を見る。プロンプトインジェクションの型 6 つと、プロンプト側・運用側の対策を
  `references/injection-cases.md` にまとめた。実際に動く攻撃文字列は載せない
- `deliverable-review-register` — `references/requirement-quality-checklist.md` を追加。
  曖昧語、未定義語、主語の欠落、検証できない要件、機能と非機能の混在、正常・異常・境界の不足、
  ID と根拠と受入条件の不足、要件間の矛盾、決定と提案と未決の混同、トレーサビリティの不足。
  各項目に誤検知を避ける条件を書いた

## 1.1.0 — 2026-09-01

提出前の機械検査を追加した。スクリプトは claude-kit の `just` から呼ぶ。

- `requirements-xlsx` — `xlsx_qa.py` を追加。数式エラー、外部リンク、非表示のシート・行・列、
  名前定義、入力規則、シート間参照、表示形式の揺れ、コメントの付いていない未決セルを検査し、
  JSON と Markdown を出す。SKILL.md の §10 を書き直し、実行できる環境の切り分けを入れた
- `pptx-house-style` — `pptx_qa.py` と `pdf_qa.py` を追加。文字切れ、フォント混在、図形の重なり、
  スライド番号、タイトル重複、出典の有無、PDF のページ数・構造・文字抽出可否を検査する。
  SKILL.md の §8 を書き直し、`pptx_audit.py`（修正前後の比較）との役割を分けた
- `qa_report.py` — 検査結果の書き出しを両スキルに同じ内容で置いた。スキル単体でも動かせるようにするため、
  共有モジュールにはしていない
- PDF は PowerPoint から書き出す方針を明記した。LibreOffice は日本語フォントが置き換わるため、
  文字切れの確認には使わない

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
