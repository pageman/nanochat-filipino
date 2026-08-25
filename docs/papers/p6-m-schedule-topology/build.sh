#!/usr/bin/env bash
# multi-format-paper-publisher pipeline (LaTeX master, embedded thebibliography)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT/paper_outputs"
# Prefer the operator Downloads tree the user opens; fall back to lowercase.
if [[ -d "$HOME/Downloads/Nanochat-Filipino" ]]; then
  DL_ROOT="$HOME/Downloads/Nanochat-Filipino/P6-M"
else
  DL_ROOT="$HOME/Downloads/nanochat-filipino/P6-M"
fi
DL_OUT="$DL_ROOT/paper_outputs"
LONG_PDF="Block Order under a Fixed English–Tagalog Token Budget - A One-Seed Schedule-Topology Study with nanochat.pdf"
mkdir -p "$OUT" "$DL_OUT" "$DL_ROOT"
cp "$ROOT/paper.tex" "$OUT/paper.tex"

if command -v tectonic >/dev/null 2>&1; then
  (cd "$OUT" && tectonic -X compile --print --keep-logs paper.tex) | tee /tmp/p6_tectonic.log
elif command -v pdflatex >/dev/null 2>&1; then
  (cd "$OUT" && pdflatex -interaction=nonstopmode paper.tex >/tmp/p6_latex1.log \
    && pdflatex -interaction=nonstopmode paper.tex >/tmp/p6_latex2.log \
    && pdflatex -interaction=nonstopmode paper.tex >/tmp/p6_latex3.log)
  cat /tmp/p6_latex3.log | tee /tmp/p6_tectonic.log
else
  echo "ERROR: no tectonic/pdflatex" >&2
  exit 1
fi

if rg -Fn 'Overfull \hbox' /tmp/p6_tectonic.log "$OUT"/paper.log 2>/dev/null; then
  echo "ERROR: Overfull \\hbox remains; fix margins before publishing." >&2
  exit 1
fi
echo "OK: no Overfull \\hbox in TeX log"

pandoc --from latex --to markdown --wrap=none "$ROOT/paper.tex" -o "$OUT/paper.md"
pandoc --from markdown --to plain --columns=80 "$OUT/paper.md" -o "$OUT/paper.txt"
pandoc --from latex --to html5 --standalone --mathjax --toc \
  --metadata title="Block Order under a Fixed English–Tagalog Token Budget v1.1" \
  "$ROOT/paper.tex" -o /tmp/p6_paper_raw.html
python3 "$ROOT/inject_css.py" /tmp/p6_paper_raw.html "$OUT/paper.html"
pandoc --from latex --to docx "$ROOT/paper.tex" -o "$OUT/paper.docx"

cp -f "$OUT"/paper.{tex,pdf,md,txt,html,docx} "$DL_OUT/"
cp -f "$OUT/paper.pdf" "$DL_OUT/$LONG_PDF"
cp -f "$ROOT/paper.tex" "$DL_ROOT/paper.tex"
echo "Wrote $OUT and $DL_OUT"
ls -lh "$DL_OUT"
