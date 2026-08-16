#!/usr/bin/env bash
# Build the DGX Spark transfer zip. Run on the Mac that holds Gates A–G.
set -euo pipefail

P1_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
STAMP="20260816"
NAME="p1.1-dgx-spark-handoff-${STAMP}"
STAGE="${P1_ROOT}/transfer/${NAME}"
DEST="${1:-/Users/paulpajo/Downloads/${NAME}.zip}"
INNER="${STAGE}/nanochat-filipino"

rm -rf "${STAGE}"
mkdir -p "${INNER}"

copy_dir() {
  local src="$1"
  local dst="$2"
  mkdir -p "$(dirname "${dst}")"
  rsync -a --copy-links "$src" "$dst"
}

# Project text/code (no secrets, no vendor venv, no Mac checkpoints)
rsync -a --exclude '.git' --exclude '.venv' --exclude '__pycache__' \
  "${P1_ROOT}/docs" "${P1_ROOT}/manifests" "${P1_ROOT}/scripts" \
  "${P1_ROOT}/patches" "${P1_ROOT}/configs" \
  "${INNER}/"
# Remove the ResearchBox passcode file if rsync copied docs/run-cards entirely
rm -f "${INNER}/docs/run-cards/aspredicted-p1-submitted.txt"

cp "${P1_ROOT}/README.md" "${P1_ROOT}/.gitignore" "${INNER}/"
mkdir -p "${INNER}/data/raw/wikitext-tl39" \
  "${INNER}/data/processed/wikitext-tl39/active" \
  "${INNER}/data/processed/wikitext-tl39/test" \
  "${INNER}/data/cache/p1-20260816T025911Z-0067a57/tokenizer" \
  "${INNER}/data/interim/wikitext-tl39/splits"

cp -p "${P1_ROOT}/data/raw/wikitext-tl39/train.parquet" "${INNER}/data/raw/wikitext-tl39/"
chmod a-w "${INNER}/data/raw/wikitext-tl39/train.parquet" || true
cp -p "${P1_ROOT}/data/processed/wikitext-tl39/active/"shard_*.parquet "${INNER}/data/processed/wikitext-tl39/active/"
cp -p "${P1_ROOT}/data/processed/wikitext-tl39/test/test.jsonl" "${INNER}/data/processed/wikitext-tl39/test/"
cp -p "${P1_ROOT}/data/processed/wikitext-tl39/test/test_manifest.json" "${INNER}/data/processed/wikitext-tl39/test/" 2>/dev/null || true
cp -p "${P1_ROOT}/data/processed/wikitext-tl39/test/README.md" "${INNER}/data/processed/wikitext-tl39/test/" 2>/dev/null || true
chmod 0444 "${INNER}/data/processed/wikitext-tl39/test/test.jsonl"
cp -p "${P1_ROOT}/data/cache/p1-20260816T025911Z-0067a57/tokenizer/tokenizer.pkl" \
  "${P1_ROOT}/data/cache/p1-20260816T025911Z-0067a57/tokenizer/token_bytes.pt" \
  "${INNER}/data/cache/p1-20260816T025911Z-0067a57/tokenizer/"
cp -p "${P1_ROOT}/data/interim/wikitext-tl39/splits/train.jsonl" \
  "${P1_ROOT}/data/interim/wikitext-tl39/splits/val.jsonl" \
  "${INNER}/data/interim/wikitext-tl39/splits/"

# Zip-root orientation files
cp "${P1_ROOT}/docs/run-cards/HANDOFF-dgx-spark-gate-h-i.md" "${STAGE}/README.md"
cp "${P1_ROOT}/docs/run-cards/HANDOFF-dgx-spark-gate-h-i.md" "${STAGE}/HANDOFF-dgx-spark-gate-h-i.md"
cp "/Users/paulpajo/Downloads/dgx_spark_gate_h_i_assessment.md" "${STAGE}/dgx_spark_gate_h_i_assessment.md"
cat > "${STAGE}/START_HERE.txt" <<'EOF'
NANOCHAT-FILIPINO P1.1 — DGX Spark transfer
==========================================
1. Read README.md (same as HANDOFF-dgx-spark-gate-h-i.md).
2. Unzip onto the Spark. Do not train yet.
3. bash nanochat-filipino/scripts/p1/setup_spark.sh
4. source nanochat-filipino/scripts/p1/env.spark.sh
5. python nanochat-filipino/scripts/p1/spark_host_preflight.py
6. Only if that exits 0: name the host, then official Gate H (p1-smoke-d4).
7. Only if H passes and preflight --require-pre-i exits 0: Gate I cards.

This zip does not contain confirmatory BPB, Mac checkpoints, or the ResearchBox passcode.
Official H/I have not started. gpu_host_for_H_I is still null.
EOF

# Checksums of payload files
(
  cd "${INNER}"
  find . -type f ! -name '.DS_Store' | sort | while read -r f; do
    shasum -a 256 "$f"
  done
) > "${STAGE}/MANIFEST.sha256"

chmod +x "${INNER}/scripts/p1/"*.sh "${INNER}/scripts/p1/"*.py || true

rm -f "${DEST}"
mkdir -p "$(dirname "${DEST}")"
(
  cd "${STAGE}/.."
  zip -r -q "${DEST}" "${NAME}"
)

echo "Wrote ${DEST}"
ls -lh "${DEST}"
echo "Excluded: vendor/.venv, Mac checkpoints, ResearchBox passcode, confirmatory weights (none exist)"
