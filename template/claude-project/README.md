# <プロジェクト名>

<!-- bin/new-claude-project で生成したひな形。見出しをプロジェクト名に書き換える -->

## このプロジェクトについて

| 項目 | 値 |
|---|---|
| 開始 | |
| 自分の役割 | 要件定義、基本設計、AI 向け詳細設計、成果物レビュー |

## ディレクトリ

| | 中身 |
|---|---|
| `00_sources/` | 受領資料と議事録 |
| `10_requirements/` | 要件、用語集、決定事項、未決事項 |
| `20_design/` | 基本設計とレビュー記録 |
| `30_prompts/` | AI 向け詳細設計とプロンプト |
| `40_evals/` | プロンプトの評価ケースと結果 |
| `50_tracking/` | 課題、進捗、トレーサビリティ、QA 記録 |
| `80_deliverables/` | 提出物 |
| `90_qa/` | 検査結果（生成物） |

扱いの詳細は各ディレクトリの README.md にある。Claude への約束は `CLAUDE.md`。

## 準備

```sh
npm ci                # textlint と markdownlint を入れる
```

## 検査

```sh
npx just qa .         # 全部
npx just qa-text .    # 日本語と Markdown だけ
npx just qa-xlsx 80_deliverables/要件定義書_20260901.xlsx
npx just qa-pptx 80_deliverables/説明資料_20260901.pptx
npx just qa-pdf  80_deliverables/説明資料_20260901.pdf
```

いずれも元ファイルを変更しない。結果は `90_qa/` に別ファイルとして出る。

終了コードは 0（指摘なし）、1（警告あり）、2（失敗）。

## 誤検知が出たとき

結果ファイルを直さない。判断した理由を `50_tracking/qa-record.md` に 1 行書く。
繰り返し出るなら `.textlintrc.json` か `prh/project-terms.yml` を直し、理由をコミットメッセージに書く。
