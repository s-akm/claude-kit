# claude-kit 検査レシピ
#
# just は入口だけを担う。検査の中身は claude-kit/bin/qa-run にある。
#
# 守ること
#   - 元ファイルを変更しない
#   - 自動修正しない
#   - 結果は <プロジェクト>/90_qa/<日時>/ に別ファイルとして出す
#
# 終了コード
#   0 指摘なし / 1 警告あり / 2 提出できない指摘あり、または実行できない

# プロジェクトをまとめて検査する（文書 ＋ 80_deliverables の成果物）
qa project=".":
    @bash "{{KIT}}/bin/qa-run" all "{{project}}"

# 日本語と Markdown だけを検査する
qa-text project=".":
    @bash "{{KIT}}/bin/qa-run" text "{{project}}"

# Excel を 1 件検査する
qa-xlsx file:
    @bash "{{KIT}}/bin/qa-run" xlsx "{{file}}"

# PowerPoint を 1 件検査する
qa-pptx file:
    @bash "{{KIT}}/bin/qa-run" pptx "{{file}}"

# PDF を 1 件検査する
qa-pdf file:
    @bash "{{KIT}}/bin/qa-run" pdf "{{file}}"

# PDF を全ページの画像とコンタクトシートにする
render-slides file:
    @bash "{{KIT}}/bin/qa-run" slides "{{file}}"
