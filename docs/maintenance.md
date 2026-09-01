# メンテナンス

## スキルの更新

プロジェクトで指摘を受けたら、該当スキルの `references/` に行を足す。静的チェックで拾える指摘なら
`template/claude-project/prh/project-terms.yml` にも足す。`plugin/CHANGELOG.md` に日付と内容を
1 行書いてコミットする。

リポジトリを直しただけでは、Claude が読むスキルは変わらない。

```sh
cd ~/workspace/claude-kit
bin/build-plugin
```

バージョンとスキル名の対応、CHANGELOG に現バージョンの見出しがあるかを検証してから、`dist/` に 2 つ出力する。
バージョン付きの名前と、常に最新を指す名前。できた `.plugin` を Claude のチャットへ渡して
インストールする。

バージョンを上げるときは `plugin/.claude-plugin/plugin.json` の `version` を直し、
`plugin/CHANGELOG.md` に同じバージョンの見出しを足す。
どちらかを忘れると `bin/build-plugin` が止まる。

チェック項目を足すときは、対象のスクリプトを修正する。

| 対象 | ファイル |
|---|---|
| Excel | `plugin/skills/requirements-xlsx/scripts/xlsx_qa.py` |
| PowerPoint | `plugin/skills/pptx-house-style/scripts/pptx_qa.py` |
| PDF | `plugin/skills/pptx-house-style/scripts/pdf_qa.py` |

修正したら `tests/fixtures/` の `ng` 側にも問題を仕込み、検出されることを確認する。
手順は [tests/README.md](../tests/README.md)。
