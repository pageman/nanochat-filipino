#!/usr/bin/env bash
# multi-format-paper-publisher pipeline (LaTeX master, no references.bib)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT/paper_outputs"
mkdir -p "$OUT"
cp "$ROOT/paper.tex" "$OUT/paper.tex"

if command -v tectonic >/dev/null 2>&1; then
  (cd "$OUT" && tectonic -X compile paper.tex)
elif command -v pdflatex >/dev/null 2>&1; then
  (cd "$OUT" && pdflatex -interaction=nonstopmode paper.tex && pdflatex -interaction=nonstopmode paper.tex && pdflatex -interaction=nonstopmode paper.tex)
else
  echo "WARN: no tectonic/pdflatex; PDF skipped" >&2
fi

pandoc --from latex --to markdown --wrap=none "$ROOT/paper.tex" -o "$OUT/paper.md"
pandoc --from markdown --to plain --columns=80 "$OUT/paper.md" -o "$OUT/paper.txt"
pandoc --from latex --to html5 --standalone --mathjax --toc \
  --metadata title="English Retention after Tagalog Continuation" \
  "$ROOT/paper.tex" -o /tmp/p2_paper_raw.html
python3 "$ROOT/inject_css.py" /tmp/p2_paper_raw.html "$OUT/paper.html"
pandoc --from latex --to docx "$ROOT/paper.tex" -o "$OUT/paper.docx"

echo "Wrote $OUT"
ls -lh "$OUT"
