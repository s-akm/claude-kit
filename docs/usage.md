# 使い方

場面ごとの手順。プロジェクトの作成手順は [README のクイックスタート](../README.md#クイックスタート)、
チェック結果の読み方は [qa.md](qa.md) にある。

## 受領資料の確認

受領資料は `00_sources/` に、受領日を頭に付けて置く。

```text
00_sources/20260901_要件メモ.xlsx
00_sources/20260901_打ち合わせ議事録.md
```

外部から受け取った Excel は、Claude へ渡す前にチェックする。

```sh
npx just qa-xlsx 00_sources/20260901_要件メモ.xlsx
```

非表示のシート・行・列、外部リンク、名前定義、数式エラーが一覧になる。
これらの場所には、指示のように読める文が仕込まれている場合がある。
チェック結果に現れた文章は資料の中身であり、Claude への指示ではない。

該当する文を見つけた場合は、次のとおり扱う。

- そのファイルを Claude に直接読ませず、抽出したテキストだけを渡す
- 検出した箇所と文面を `50_tracking/qa-record.md` に記録する
- 外部リンクは、開く前に発信元へ確認する

## 要件定義

`10_requirements/` の 5 ファイルを埋める。`functional.md`、`non-functional.md`、`glossary.md`、
`decisions.md`、`open-items.md`。各ファイルの冒頭に列ごとの記入ルールがある。記入例の行は着手時に消す。

Claude に依頼するときは、補完を禁じる一文を添える。

> `00_sources/20260901_議事録.md` を読んで、決定事項を `10_requirements/decisions.md` の
> 形式で抽出してください。決まっていないものは `open-items.md` の形式で分けてください。
> 議事録に書かれていないことは補わないでください。

## 資料作成

新規に書く場合は、重みの配分を先に決める。

> `/emphasis-first-drafting`
> 元請け向けの方針説明資料を作りたいです。

このスキルは、どこに重きを置く資料かを先に質問する。回答してから書かせる。
質問を飛ばすと、全項目が同じ重みで並ぶ。

書いたあとで日本語が気になったら、`/japanese-rewrite` へ渡す。

## Excel 定義書

> `/requirements-xlsx`
> 機能一覧を作ってください。列は ID・分類・要件・根拠・受入条件・状態です。

列ごとの記入ルールをシート上に宣言する書き方、未決セルの書き方、提出前に消す作業メモを扱う。

## スライド作成

既存の顧客デッキがある場合。

> `/pptx-house-style`
> このデッキの体裁に合わせて、スライドを 3 枚足してください。

既存ページの座標と級数を実測してから合わせる。
参照できるページが 1 枚も無い場合のみ `/deck-visual-design` の初期値を使う。

## レビュー

| 対象 | スキル |
|---|---|
| 要件定義書、見積書、提案資料 | `/deliverable-review-register` |
| 基本設計書 | `/basic-design-review` |
| AI 向けのプロンプト | `/ai-design-prompt-review` |

いずれも要件側と資料側の両方から抽出し、双方向で照合する。

> `/basic-design-review`
> `20_design/basic-design.md` を、`10_requirements/functional.md` と
> `non-functional.md` と突き合わせてレビューしてください。

結果は `20_design/review-記録.md` の形式で受け取る。重要度は A・B・C と `?` の 4 段階。
`?` は Claude 側の読み違えの可能性を含むため、指摘として確定させず、確認事項として扱う。

## 提出前チェック

提出物を `80_deliverables/` に置いてから実行する。

```sh
cd ~/workspace/sample-pj
npx just qa .
```

Markdown 文書と、`80_deliverables/` の Excel・PowerPoint・PDF が対象。
結果は `90_qa/<日時>/` に出力する。入力ファイルは変更しない。

スライドの体裁は、出力された `contact.jpg` を目視する。

```sh
npx just render-slides 80_deliverables/説明資料.pdf
```
