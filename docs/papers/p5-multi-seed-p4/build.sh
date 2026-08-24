#!/usr/bin/env bash
# multi-format-paper-publisher pipeline (LaTeX master, embedded thebibliography)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT/paper_outputs"
DL_OUT="$HOME/Downloads/nanochat-filipino/p5/paper_outputs"
mkdir -p "$OUT" "$DL_OUT"
cp "$ROOT/paper.tex" "$OUT/paper.tex"

if command -v tectonic >/dev/null 2>&1; then
  (cd "$OUT" && tectonic -X compile paper.tex)
elif command -v pdflatex >/dev/null 2>&1; then
  (cd "$OUT" && pdflatex -interaction=nonstopmode paper.tex >/tmp/p5_latex1.log \
    && pdflatex -interaction=nonstopmode paper.tex >/tmp/p5_latex2.log \
    && pdflatex -interaction=nonstopmode paper.tex >/tmp/p5_latex3.log)
else
  echo "ERROR: no tectonic/pdflatex" >&2
  exit 1
fi

pandoc --from latex --to markdown --wrap=none "$ROOT/paper.tex" -o "$OUT/paper.md"
pandoc --from markdown --to plain --columns=80 "$OUT/paper.md" -o "$OUT/paper.txt"
pandoc --from latex --to html5 --standalone --mathjax --toc \
  --metadata title="How Often a Frozen Mix Recurs across Unused Initializations" \
  "$ROOT/paper.tex" -o /tmp/p5_paper_raw.html
python3 "$ROOT/inject_css.py" /tmp/p5_paper_raw.html "$OUT/paper.html"
pandoc --from latex --to docx "$ROOT/paper.tex" -o "$OUT/paper.docx"

cp -f "$OUT"/paper.{tex,pdf,md,txt,html,docx} "$DL_OUT/"
echo "Wrote $OUT and $DL_OUT"
ls -lh "$DL_OUT"
