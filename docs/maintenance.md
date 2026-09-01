# メンテナンス

## スキルの更新

プロジェクトで指摘を受けた際の手順。

1. 該当スキルの `references/` に行を追加
2. 静的チェックで拾える指摘は `template/claude-project/prh/project-terms.yml` にも追加
3. `plugin/CHANGELOG.md` に日付と内容を 1 行記載
4. コミット

リポジトリの修正のみでは、Claude が読むスキルは未変更のまま。

```sh
cd ~/workspace/claude-kit
bin/build-plugin
```

バージョンとスキル名の対応、CHANGELOG への現バージョンの見出しの有無を検証後、`dist/` に 2 つ出力。
バージョン付きの名前と、常に最新を指す名前。できた `.plugin` を Claude のチャットへ渡してインストール。

## バージョン運用

`plugin/.claude-plugin/plugin.json` の `version` と、`plugin/CHANGELOG.md` の見出しを同時に更新。
片方が欠けた場合は `bin/build-plugin` が中断。

## チェック項目の追加

| 対象 | ファイル |
|---|---|
| Excel | `plugin/skills/requirements-xlsx/scripts/xlsx_qa.py` |
| PowerPoint | `plugin/skills/pptx-house-style/scripts/pptx_qa.py` |
| PDF | `plugin/skills/pptx-house-style/scripts/pdf_qa.py` |

修正後、`tests/fixtures/` の `ng` 側にも該当する問題を仕込み、検出を確認。
手順は [tests/README.md](../tests/README.md) を参照。
