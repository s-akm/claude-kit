# 導入と運用

## 1. 新しい端末で使えるようにする

```sh
cd ~/workspace
git clone <このリポジトリ> claude-kit
```

案件は `~/workspace/<案件名>` に置く。kit と案件が同じ親ディレクトリにあることを前提に、
生成される `justfile` は `../claude-kit` を相対で参照する。

### 必要なコマンド

| コマンド | 用途 | 導入 |
|---|---|---|
| Node.js 22 以上 | textlint、markdownlint、just | mise |
| Python 3.10 以上 | 検査スクリプト | mise |
| `just` | 検査の入口 | 各案件の `npm ci` で入る（`rust-just`）。brew は不要 |
| `poppler` | PDF をページ画像にする | `brew install poppler` |
| `qpdf` | PDF の構造検査 | `brew install qpdf` |
| `imagemagick` | コンタクトシートの合成 | `brew install imagemagick` |

`just` は npm から入るため、Homebrew で入れる必要はない。
`poppler`、`qpdf`、`imagemagick` の 3 つは、PDF とスライドのチェックで使う。

### LibreOffice は入れない

pptx を PDF にする用途で LibreOffice を使う手はあるが、日本語フォントが Mac と違うため、
文字幅が変わって「文字切れ」の検査が当てにならなくなる。
**体裁を見るための PDF は PowerPoint から書き出す。**

## 2. 新しい案件を作る

```sh
~/workspace/claude-kit/bin/new-claude-project <案件名>          # 表示のみ
~/workspace/claude-kit/bin/new-claude-project <案件名> --apply  # 作成
cd ~/workspace/<案件名> && npm ci
```

既定は表示のみ。既に同名のディレクトリがある場合は何もしない。

## 3. 検査する

```sh
cd ~/workspace/<案件名>
npx just qa .
```

元ファイルは変更しない。結果は `90_qa/<日時>/` に別ファイルで出る。

終了コードは 0（指摘なし）、1（警告あり）、2（失敗）。

### どこから実行できるか

| 実行元 | `just` を呼べるか |
|---|---|
| ターミナル | 呼べる |
| Cowork（案件フォルダを接続している場合） | 呼べる |
| Claude デスクトップ単体 | **呼べない**。人が実行し、`90_qa/` の結果を読ませる |
| Office アドイン（Excel・PowerPoint・Word） | **呼べない**。同上 |

スキルは 4 つとも同じものが使われるが、ローカルコマンドを実行できるのは上の 2 つだけ。

## 4. 誤検知が出たとき

自動修正はしない。`textlint --fix` も既定では走らせない。

| 状況 | 対応 |
|---|---|
| その 1 件だけ | `50_tracking/qa-record.md` に、なぜ問題ないと判断したかを 1 行書く |
| 特定のファイル全体 | ファイル先頭に `<!-- textlint-disable ルール名 -->` を書く |
| 案件全体で繰り返す | `.textlintrc.json` か `prh/project-terms.yml` を直し、理由をコミットメッセージに書く |

`10_requirements/glossary.md` は「使わない語」を列に書くため、既定で prh の対象から外してある。

## 5. スキルを直したあとにやること

リポジトリを直しただけでは、Claude が読むスキルは変わらない。
手順は [maintenance.md](maintenance.md) にある。

## 6. Office アドインから使う

Excel・PowerPoint・Word のアドインでも、有効にしたスキルがそのまま使える。
導入の手順、スキルの呼び方、外部から受け取った Excel の安全なレビュー手順は
`docs/claude-for-m365.md` にまとめてある。

アドインからは `just` を呼べない。人が端末で実行し、`90_qa/` の結果を読ませる。

## 7. やらないこと

- 元ファイルを変更しない
- 自動修正しない
- 顧客データと認証情報を Git に入れない
- 指示がない限り commit、push、外部への送信をしない
