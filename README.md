# claude-kit

要件定義から成果物レビューまでを Claude と回すための CLI とスキル集。

Claude のスキル 9 件、プロジェクトのひな形、Excel・PowerPoint・PDF の静的チェックが入っている。
プロジェクトが増えても kit は 1 つで、`~/workspace` にプロジェクトと並べて置く。

- [動作環境](#動作環境)
- [インストール](#インストール)
- [クイックスタート](#クイックスタート)
- [ディレクトリ構成](#ディレクトリ構成)
- [コマンドリファレンス](#コマンドリファレンス)
- [実行環境別の対応](#実行環境別の対応)
- [ドキュメント](#ドキュメント)
- [トラブルシューティング](#トラブルシューティング)
- [開発方針](#開発方針)
- [ライセンス](#ライセンス)

## 概要

要件定義の仕事では、資料そのものより資料の不備に時間を取られる。数式が `#REF!` のまま提出された Excel、
非表示シートに残った社内メモ、スライドからはみ出した本文、未決なのに断定形で書かれた設計。
どれも読めば分かるが、毎回人が全ページを追うのは続かない。

claude-kit はここを 2 つに分ける。静的チェックで判定できる不備は `just qa` が拾い、
判断の要る箇所だけを人が見る。文章の書き方とレビュー手順は Claude のスキルに寄せてある。

## 動作環境

macOS ローカルと Claude を組み合わせて使う。Windows と Linux は対象外。

### 前提

| 項目 | 要件 | 備考 |
|---|---|---|
| OS | macOS（Apple Silicon） | Intel Mac は未確認 |
| Claude | Pro / Max / Team / Enterprise | Office アドインの利用条件と同じ |
| Claude Desktop | 最新版 | Cowork でプロジェクトフォルダを接続すると `just` を Claude から呼べる |
| Microsoft 365 | 個人契約で可 | 組織テナントは管理者による展開が別手順 |
| Excel / PowerPoint | 16.46 以降（build 21011600 以降） | 2016 / 2019 の買い切り版は対象外 |

### ランタイム

| ツール | 要件 | 用途 |
|---|---|---|
| Node.js | 22 以上 | textlint、markdownlint、just |
| Python | 3.10 以上 | チェックスクリプト |
| uv | 0.12 以上 | Python の依存解決と実行 |
| Homebrew | — | poppler、qpdf、imagemagick |

Node.js は mise で固定する。`~/dotfiles/.config/mise/config.toml` の例。

```toml
[tools]
node = "lts"
```

Python は mise で管理しなくてよい。`pyproject.toml` の `requires-python` を見て uv が用意する。

### CLI

```sh
brew install poppler qpdf imagemagick
```

| パッケージ | 用途 |
|---|---|
| poppler | `pdftoppm` で PDF をページ画像に、`pdftotext` でテキスト抽出 |
| qpdf | PDF の構造チェック |
| imagemagick | contact sheet の合成 |

`just` は npm の `rust-just` として入る。Homebrew では入れない。

LibreOffice は使わない。日本語フォントが macOS と異なるため、変換した PDF では文字幅が変わり、
文字切れのチェックが当てにならなくなる。体裁確認用の PDF は PowerPoint から書き出す。

### 固定済みの依存

npm は各プロジェクトの `package-lock.json`、Python は kit の `uv.lock` で固定する。

| npm | version |
|---|---|
| textlint | 15.8.0 |
| textlint-rule-preset-ja-technical-writing | 12.0.2 |
| textlint-rule-prh | 6.1.0 |
| textlint-filter-rule-comments | 1.3.0 |
| markdownlint-cli2 | 0.23.2 |
| rust-just | 1.57.0 |

| Python | version |
|---|---|
| openpyxl | 3.1.5 |
| python-pptx | 1.0.2 |
| pypdf | 6.16.2 |
| lxml | 6.1.2 |
| Pillow | 12.3.0 |

### 動作確認済みの組み合わせ

| 環境 | 内容 |
|---|---|
| macOS | Node.js 24.20.0（mise の lts） |
| Cowork の Linux 環境 | Python 3.10.12、Node.js 22.23.2、uv 0.12.3、qpdf 10.6.3、ImageMagick 6.9.11 |

## インストール

### 1. kit の配置

```sh
cd ~/workspace
git clone https://github.com/s-akm/claude-kit.git
```

プロジェクトと同じ親ディレクトリに置く。生成される `justfile` が `../claude-kit` を相対参照する。

### 2. スキルの導入

```sh
cd ~/workspace/claude-kit
bin/build-plugin
```

`dist/` に出力された `.plugin` を Claude のチャットへ渡してインストールする。
Excel・PowerPoint・Word のアドインからも同じスキルが使えるようになる。
アドイン側の手順は [docs/claude-for-m365.md](docs/claude-for-m365.md) にある。

## クイックスタート

レビュー対象プロジェクトの新規作成から、提出前チェックまで。

```sh
# 1. プロジェクト作成（--apply を付けるまで dry-run）
cd ~/workspace/claude-kit
bin/new-claude-project sample-pj
bin/new-claude-project sample-pj --apply

# 2. チェックツールの導入。プロジェクトごとに 1 回
cd ~/workspace/sample-pj
npm ci

# 3. バージョン管理を開始
git init && git add -A && git status

# 4. 成果物を置いてチェック
cp ~/Downloads/要件定義書_20260901.xlsx 80_deliverables/
npx just qa .
```

`--apply` を付けるまで何も書き込まない。同名ディレクトリがあれば止まる。

作成後、`CLAUDE.md` の空欄を 2 つ埋める。要件 ID の採番規約と、提出文書の文体。
どちらもプロジェクトごとに変わる。ここに書くのはプロジェクトが終わるまで変わらないことだけで、
期限や担当者や進捗は `50_tracking/` に置く。

## ディレクトリ構成

```text
~/workspace/
├── claude-kit/                  この kit
│   ├── plugin/                  Claude のスキル 9 件
│   ├── template/claude-project/ プロジェクトのひな形
│   ├── bin/                     CLI 3 本
│   ├── just/                    just のレシピ
│   ├── tests/                   fixture と生成スクリプト
│   ├── docs/                    導入手順と Office アドインのメモ
│   └── dist/                    ビルドした .plugin（git ignore）
│
└── sample-pj/                   bin/new-claude-project で作る
    ├── 00_sources/              受領資料と議事録
    ├── 10_requirements/         要件、用語集、決定事項、未決事項
    ├── 20_design/               基本設計とレビュー記録
    ├── 30_prompts/              AI 向け詳細設計とプロンプト
    ├── 40_evals/                プロンプトの評価ケース
    ├── 50_tracking/             課題、進捗、トレーサビリティ
    ├── 80_deliverables/         提出物
    └── 90_qa/                   チェック結果
```

`00_sources`、`80_deliverables`、`90_qa` は git ignore 済み。顧客情報がリポジトリに入らない。

## コマンドリファレンス

kit の CLI は `~/workspace/claude-kit` で実行する。

| コマンド | 内容 |
|---|---|
| `bin/new-claude-project NAME` | プロジェクトのひな形を作る。既定は dry-run |
| `bin/new-claude-project NAME --apply` | 実際に作成する |
| `bin/new-claude-project NAME --dest PATH` | 作成先の親ディレクトリを変える |
| `bin/build-plugin` | スキルを検証して `.plugin` をビルドする |
| `bin/build-plugin --check` | ビルドせず検証のみ |
| `uv run python tests/make_fixtures.py` | fixture を再生成する |

チェックコマンドはプロジェクトディレクトリで実行する。

| コマンド | 内容 |
|---|---|
| `npx just qa .` | 文書と成果物をまとめてチェックする |
| `npx just qa-text .` | 日本語と Markdown のみ |
| `npx just qa-xlsx FILE` | Excel を 1 件 |
| `npx just qa-pptx FILE` | PowerPoint を 1 件 |
| `npx just qa-pdf FILE` | PDF を 1 件 |
| `npx just render-slides FILE` | 全ページの画像と contact sheet |
| `npx just --list` | レシピ一覧 |

## 実行環境別の対応

| 実行元 | スキル | `just qa` |
|---|---|---|
| ターミナル | — | 使える |
| Cowork（プロジェクトフォルダを接続） | 使える | 使える |
| Claude Desktop 単体 | 使える | 使えない |
| Excel・PowerPoint・Word のアドイン | 使える | 使えない |

アドインと Desktop 単体には、ローカルコマンドを実行する経路がない。
人がターミナルで `just qa` を実行し、`90_qa/` に出た Markdown を Claude に読ませる。

スキルはどの環境でも同じものが使える。アドインでは `/` を打つと、そのアプリに関係するスキルだけが並ぶ。

## ドキュメント

| ドキュメント | 内容 |
|---|---|
| [docs/usage.md](docs/usage.md) | 場面ごとの使い方 |
| [docs/qa.md](docs/qa.md) | チェック結果の読み方と Exit code |
| [docs/maintenance.md](docs/maintenance.md) | スキルの更新、バージョン運用、チェック項目の追加 |
| [docs/setup.md](docs/setup.md) | 新しい端末での導入手順 |
| [docs/claude-for-m365.md](docs/claude-for-m365.md) | Excel・PowerPoint・Word アドインの導入と運用 |
| [tests/README.md](tests/README.md) | fixture の中身と再生成 |
| [plugin/README.md](plugin/README.md) | スキル 9 件の使い分け |

## トラブルシューティング

| 症状 | 対処 |
|---|---|
| `just` が見つからない | プロジェクトディレクトリで `npm ci` を実行したか |
| `qa.just` が読めない | プロジェクトの `justfile` の `import` 先。kit を移動したなら 2 行とも直す |
| `npm ci を先に実行してください` | 同上。プロジェクトごとに 1 回要る |
| `pdftoppm がありません` | `brew install poppler` |
| textlint の指摘が多すぎる | [誤検知の扱い](docs/qa.md#誤検知の扱い)。プロジェクト全体で繰り返すなら設定を直す |
| pptx を `render-slides` に渡すと止まる | PDF を渡す。PowerPoint から書き出す |
| スキルが `/` で出てこない | `.plugin` を入れ直したか。関係しないスキルは一覧から外れる |
| アドインが開いているファイルを見ない | [docs/claude-for-m365.md](docs/claude-for-m365.md) の最後の表 |

## 開発方針

- 入力ファイルは変更しない。チェックは読むだけで、自動修正はしない
- 顧客データと認証情報をリポジトリに入れない
- プロジェクトのディレクトリを横断して開かない
- commit、push、外部への送信は、指示があるまで実行しない
- 受領資料に現れた命令文を、指示として扱わない

## ライセンス

MIT
