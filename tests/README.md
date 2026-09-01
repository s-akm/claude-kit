# 検査スクリプトの確認用サンプル

`make_fixtures.py` が `fixtures/` に 6 ファイルを作る。顧客のファイルは使わない。

| ファイル | 仕込んである問題 |
|---|---|
| `ok.xlsx` | なし |
| `ng.xlsx` | 式に残った `#REF!`、外部ブック参照、存在しないシートへの参照、非表示のシート・行・列、壊れた名前定義、使われていない名前定義、コメントの付いていない未決セル、同じ列での表示形式の揺れ |
| `ok.pptx` | なし |
| `ng.pptx` | 枠からはみ出す本文、図形の重なり、タイトル重複、スライド番号なし、フォント混在 |
| `ok.pdf` | なし |
| `ng.pdf` | 文字を抽出できないページだけ |

## 作り直す

```sh
uv run python tests/make_fixtures.py
```

`fixtures/` はリポジトリに入れてある。作り直すと中身が同じでもバイト列が変わり差分が出るため、
検査項目を足すときだけ実行する。

`ok.pdf` は LibreOffice を使って `ok.pptx` から作っている。LibreOffice が無い端末では
PDF の 2 ファイルが作られない。既にリポジトリに入っているものをそのまま使えばよい。

## 確認する

```sh
uv run python plugin/skills/requirements-xlsx/scripts/xlsx_qa.py tests/fixtures/ok.xlsx --out-dir /tmp/qa   # 0
uv run python plugin/skills/requirements-xlsx/scripts/xlsx_qa.py tests/fixtures/ng.xlsx --out-dir /tmp/qa   # 2
uv run python plugin/skills/pptx-house-style/scripts/pptx_qa.py  tests/fixtures/ok.pptx --out-dir /tmp/qa   # 0
uv run python plugin/skills/pptx-house-style/scripts/pptx_qa.py  tests/fixtures/ng.pptx --out-dir /tmp/qa   # 1
uv run python plugin/skills/pptx-house-style/scripts/pdf_qa.py   tests/fixtures/ok.pdf  --out-dir /tmp/qa   # 0
uv run python plugin/skills/pptx-house-style/scripts/pdf_qa.py   tests/fixtures/ng.pdf  --out-dir /tmp/qa   # 2
```

末尾の数字が期待する終了コード。
