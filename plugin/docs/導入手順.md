# 導入手順

## A. Cowork / Claude デスクトップアプリへ入れる

1. `jp-client-deliverables.plugin` をチャットへ添付する
2. プレビューカードの内容を確認し、インストールを押す
3. スキルの一覧に7件が追加される

## B. Claude Code へ入れる（プラグインとして）

```bash
unzip jp-client-deliverables.plugin -d ~/.claude/plugins/jp-client-deliverables
```

`~/.claude/plugins/jp-client-deliverables/.claude-plugin/plugin.json` が存在すれば読み込まれる。

## C. スキル単体で置く

プラグインの仕組みを使わず、スキルだけ置くこともできる。

```bash
unzip jp-client-deliverables.plugin -d /tmp/jpkit
cp -r /tmp/jpkit/skills/* ~/.claude/skills/
```

この場合、スキル間の相互参照（`japanese-business-writing/references/...` のような記述）は
相対パスではなくスキル名で辿ることになる。Claude はスキル名で探せるため、動作は変わらない。

## D. リポジトリとして運用する

このディレクトリは git リポジトリになっている。プロジェクトごとに指摘を足していく前提のため、
配布物をそのまま置くのではなく、リポジトリを clone して使うほうが差分を追いやすい。

```bash
git clone <リモート> jp-client-deliverables
cd jp-client-deliverables
```

プロジェクトで新しい指摘を受けたら、次の順で反映する。

1. 該当するスキルの `references/` に行を足す
2. 機械走査で拾える指摘なら `patterns.json` にも足す
3. `CHANGELOG.md` に日付と内容を1行書く
4. コミットする

### 再パッケージ

```bash
cd jp-client-deliverables
zip -r /tmp/jp-client-deliverables.plugin . \
  -x "*.DS_Store" -x "*.git/*" -x "*__pycache__/*" -x "*.plugin"
```

`/tmp` で作ってから配布先へコピーする。

## スクリプトの依存関係

```bash
pip3 install python-pptx lxml Pillow
```

`scan_expressions.py` と `xlsx_open_items.py` は標準ライブラリだけで動くため、
インストールなしで使える。pptx 系のスクリプトだけ上記が要る。

`contact_sheet.py` は事前に LibreOffice と poppler-utils が要る。

```bash
soffice --headless --convert-to pdf deck.pptx --outdir .
pdftoppm -r 90 -jpeg deck.pdf page
```

## 動作確認

```bash
python3 skills/japanese-business-writing/scripts/scan_expressions.py README.md
python3 skills/requirements-xlsx/scripts/xlsx_open_items.py 任意の.xlsx
```

前者は README に含まれる記号などを拾って件数を返す。後者は未決セルとコメントを一覧する。
どちらもエラーなく終われば導入できている。
