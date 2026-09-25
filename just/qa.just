# claude-kit チェックレシピ
#
# just は入口のみ。処理の実体は claude-kit/bin/qa-run。
#
# 守ること
#   - 入力ファイルは変更しない
#   - 自動修正なし
#   - 出力先は <プロジェクト>/90_qa/<日時>/。別ファイルとして書き出し
#
# Exit code
#   0 指摘なし / 1 警告あり / 2 提出不可の指摘あり、または実行不可

# プロジェクトの一括チェック（文書 ＋ 80_deliverables の成果物）
qa project=".":
    @bash "{{KIT}}/bin/qa-run" all "{{project}}"

# 日本語と Markdown のみ
qa-text project=".":
    @bash "{{KIT}}/bin/qa-run" text "{{project}}"

# Excel を 1 件
qa-xlsx file:
    @bash "{{KIT}}/bin/qa-run" xlsx "{{file}}"

# PowerPoint を 1 件
qa-pptx file:
    @bash "{{KIT}}/bin/qa-run" pptx "{{file}}"

# PDF を 1 件
qa-pdf file:
    @bash "{{KIT}}/bin/qa-run" pdf "{{file}}"

# PDF を全ページの画像と contact sheet へ変換
render-slides file:
    @bash "{{KIT}}/bin/qa-run" slides "{{file}}"
