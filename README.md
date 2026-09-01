# claude-kit

要件定義・基本設計・AI向け詳細設計と、Excel／PowerPoint 成果物のレビューを回すための道具一式。
案件ディレクトリ（`~/workspace/<案件名>`）とは別に置き、案件をまたいで使う。

## 構成

| ディレクトリ | 中身 |
|---|---|
| `plugin/` | Claude のスキル本体。ここを zip して `.plugin` を作る |
| `just/` | 検査コマンドの実体。各案件の `justfile` から読み込む |
| `template/claude-project/` | 新規案件のひな形 |
| `bin/` | 案件生成スクリプト |
| `tests/` | 検査スクリプトの確認用サンプルと生成コード |
| `docs/` | 導入手順と、Claude for Microsoft 365 の運用メモ |

## 新規案件を作る

```sh
bin/new-claude-project <案件名>          # 何を作るか表示するだけ
bin/new-claude-project <案件名> --apply  # 実際に作る
```sh

既定は表示のみ。`--apply` を付けたときだけ書き込む。既に同名のディレクトリがある場合は何もしない。

## スキルを直したあとにやること

リポジトリを直しただけでは、Claude デスクトップと Office アドインが読むスキルは変わらない。
手順は `docs/setup.md` の「.plugin の作り直し」を見る。

## この kit が守ること

- 元ファイルを変更しない。検査は読むだけで、自動修正はしない
- 顧客データと認証情報を Git に入れない
- 案件のディレクトリを横断して開かない
