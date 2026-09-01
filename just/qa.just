# claude-kit 検査レシピ
#
# 守ること
#   - 元ファイルを変更しない
#   - 自動修正しない
#   - 結果は <project>/90_qa/<日時>/ に別ファイルとして出す
#
# 終了コード
#   0 指摘なし / 1 警告あり / 2 失敗

# 全部を検査する
qa project=".":
    @just qa-text "{{project}}"

# 日本語と Markdown を検査する
qa-text project=".":
    #!/usr/bin/env bash
    set -uo pipefail
    cd "{{project}}" || { echo "ディレクトリがありません: {{project}}" >&2; exit 2; }
    if [ ! -d node_modules ]; then echo "npm ci を先に実行してください" >&2; exit 2; fi
    ts=$(date +%Y-%m-%d-%H%M)
    out="90_qa/$ts"
    mkdir -p "$out"
    targets=(10_requirements 20_design 30_prompts 50_tracking README.md CLAUDE.md)
    exist=()
    for t in "${targets[@]}"; do [ -e "$t" ] && exist+=("$t"); done

    {
      echo "実行日時   $(date '+%Y-%m-%d %H:%M:%S %z')"
      echo "対象       $(pwd)"
      echo "node       $(node --version 2>/dev/null)"
      echo "textlint   $(npx --no-install textlint --version 2>/dev/null)"
      echo "mdlint     $(npx --no-install markdownlint-cli2 --version 2>/dev/null | head -1)"
    } > "$out/text-meta.txt"

    rc=0
    npx --no-install textlint -f json "${exist[@]}" > "$out/text.json" 2>"$out/text-stderr.txt" || rc=1
    npx --no-install textlint "${exist[@]}" > "$out/text-textlint.txt" 2>&1 || true
    npx --no-install markdownlint-cli2 > "$out/text-markdownlint.txt" 2>&1 || rc=1

    {
      echo "# 文書検査の結果"
      echo
      cat "$out/text-meta.txt" | sed 's/^/    /'
      echo
      echo "## textlint"
      echo
      echo '```'
      cat "$out/text-textlint.txt"
      echo '```'
      echo
      echo "## markdownlint"
      echo
      echo '```'
      cat "$out/text-markdownlint.txt"
      echo '```'
      echo
      echo "## 誤検知だと判断したとき"
      echo
      echo "この結果ファイルを直さない。判断の理由を 50_tracking/qa-record.md に 1 行書く。"
      echo "繰り返し出るなら .textlintrc.json か prh/project-terms.yml を直す。"
    } > "$out/text.md"

    echo "結果: $(pwd)/$out"
    exit $rc

# Excel を検査する
qa-xlsx file:
    @echo "未実装（Phase 3 で追加する）: {{file}}" >&2
    @exit 2

# PowerPoint を検査する
qa-pptx file:
    @echo "未実装（Phase 3 で追加する）: {{file}}" >&2
    @exit 2

# PDF を検査する
qa-pdf file:
    @echo "未実装（Phase 3 で追加する）: {{file}}" >&2
    @exit 2

# スライドを画像とコンタクトシートにする
render-slides file:
    @echo "未実装（Phase 3 で追加する）: {{file}}" >&2
    @exit 2
