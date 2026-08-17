#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT/manifest_outputs"
mkdir -p "$OUT"
SRC="$ROOT/additions-manifest.tex"
cp "$SRC" "$OUT/additions-manifest.tex"

if command -v tectonic >/dev/null 2>&1; then
  (cd "$OUT" && tectonic -X compile additions-manifest.tex)
elif command -v pdflatex >/dev/null 2>&1; then
  (cd "$OUT" && pdflatex -interaction=nonstopmode additions-manifest.tex && pdflatex -interaction=nonstopmode additions-manifest.tex)
else
  echo "WARN: no tectonic/pdflatex; PDF skipped" >&2
fi

pandoc --from latex --to markdown --wrap=none "$SRC" -o "$OUT/additions-manifest.md"
pandoc --from markdown --to plain --columns=80 "$OUT/additions-manifest.md" -o "$OUT/additions-manifest.txt"
pandoc --from latex --to html5 --standalone --mathjax --toc \
  --metadata title="Additions Manifest for a Tagalog-English Catastrophic Forgetting Paper" \
  "$SRC" -o /tmp/p2_manifest_raw.html
python3 "$ROOT/inject_css.py" /tmp/p2_manifest_raw.html "$OUT/additions-manifest.html"
pandoc --from latex --to docx "$SRC" -o "$OUT/additions-manifest.docx"

echo "Wrote $OUT"
ls -lh "$OUT"
