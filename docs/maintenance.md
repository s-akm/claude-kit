# メンテナンス

## スキルの更新

プロジェクトで指摘を受けたら、該当スキルの `references/` に行を足す。
静的チェックで拾える指摘は `template/claude-project/prh/project-terms.yml` にも足す。
`plugin/CHANGELOG.md` に日付と内容を 1 行書いてコミットする。

リポジトリの修正だけでは、Claude が読むスキルは変わらない。

```sh
cd ~/workspace/claude-kit
bin/build-plugin
```

バージョンとスキル名の対応、CHANGELOG に現バージョンの見出しがあるかを検証してから、
`dist/` にバージョン付きの名前と、常に最新を指す名前の 2 つを出力する。
できた `.plugin` を Claude のチャットへ渡してインストールする。

## バージョン運用

`plugin/.claude-plugin/plugin.json` の `version` と、`plugin/CHANGELOG.md` の見出しを同時に更新する。
どちらかが欠けると `bin/build-plugin` が中断する。

## チェック項目の追加

| 対象 | ファイル |
|---|---|
| Excel | `plugin/skills/requirements-xlsx/scripts/xlsx_qa.py` |
| PowerPoint | `plugin/skills/pptx-house-style/scripts/pptx_qa.py` |
| PDF | `plugin/skills/pptx-house-style/scripts/pdf_qa.py` |

修正後、`tests/fixtures/` の `ng` 側にも該当する問題を仕込み、検出されることを確認する。
手順は [tests/README.md](../tests/README.md)。
