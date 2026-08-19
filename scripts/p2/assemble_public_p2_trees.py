#!/usr/bin/env python3
"""Copy public P2 receipts into results/p2 and docs/hub/p2-en-then-tl. No .pt, test.jsonl, passcodes, HOST cards."""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path("/Users/paulpajo/Projects/nanochat-filipino")
CARDS = ROOT / "docs/run-cards/p2/p2-20260817T150944Z-de99f8a"
PAPER = ROOT / "docs/papers/p2-cf-english"
RESULTS = ROOT / "results/p2"
HUB = ROOT / "docs/hub/p2-en-then-tl"
EXCLUDE = {"HOST-8ik4ix7j8iju9u.md", "HOST-xk8orhscuk2jsu.md"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def copy(src: Path, dest: Path) -> None:
    if src.name in EXCLUDE:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def dump(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n")


def main() -> None:
    if RESULTS.exists():
        shutil.rmtree(RESULTS)
    if HUB.exists():
        shutil.rmtree(HUB)
    RESULTS.mkdir(parents=True)
    eval_dir = RESULTS / "evaluation"
    eval_dir.mkdir()

    seal = json.loads((CARDS / "gate-u-seal.json").read_text())
    copy(CARDS / "gate-u-seal.json", RESULTS / "gate-u-seal.json")
    copy(CARDS / "gate-v-test.json", RESULTS / "gate-v-test.json")
    copy(ROOT / "docs/run-cards/p2/test_access_log.json", RESULTS / "test_access_log.json")
    copy(CARDS / "gate_p0_val_baselines.json", RESULTS / "gate_p0_val_baselines.json")
    copy(CARDS / "p2-en0-d20_p0e_val.json", RESULTS / "p2-en0-d20_p0e_val.json")
    copy(CARDS / "p2-en0-d8_p0e_val.json", RESULTS / "p2-en0-d8_p0e_val.json")
    copy(CARDS / "p2-en0-d20_a0_tagalog_val.json", RESULTS / "p2-en0-d20_a0_tagalog_val.json")
    copy(CARDS / "gate-q-a0.json", RESULTS / "gate-q-a0.json")
    copy(CARDS / "gate-r-a1.json", RESULTS / "gate-r-a1.json")
    copy(CARDS / "gate-s-a2.json", RESULTS / "gate-s-a2.json")
    copy(CARDS / "gate-t-a3.json", RESULTS / "gate-t-a3.json")
    copy(CARDS / "gate-e-shards.json", RESULTS / "gate-e-shards.json")
    copy(CARDS / "registered-reporting-q3-q8.json", RESULTS / "registered-reporting-q3-q8.json")
    copy(CARDS / "byte_unigram_english_val.json", RESULTS / "byte_unigram_english_val.json")
    lock = json.loads((PAPER / "LOCK.json").read_text())
    lock.pop("researchbox_passcode", None)
    dump(RESULTS / "LOCK.sanitized.json", lock)

    for arm in ("A1", "A2", "A3"):
        cell = seal["cells"][arm]
        dump(eval_dir / f"{arm.lower()}_english_val.json", {"arm": arm, "language": "english", "split": "val", **cell["english"]})
        dump(eval_dir / f"{arm.lower()}_tagalog_val.json", {"arm": arm, "language": "tagalog", "split": "val", **cell["tagalog"]})

    table = seal["table_d20"]
    with (RESULTS / "sealed_val_table.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["arm", "english_val_bpb_full", "tagalog_val_bpb_full"])
        for arm in ("Untrained", "A0", "A1", "A2", "A3"):
            cell = table[arm]
            w.writerow([arm, cell.get("english_val_bpb_full") or "", cell.get("tagalog_val_bpb_full") or ""])

    reporting = json.loads((CARDS / "registered-reporting-q3-q8.json").read_text())
    with (RESULTS / "exposure_by_arm.csv").open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "arm",
                "stream",
                "unique_documents",
                "canonical_utf8_bytes",
                "unique_bpe_tokens_no_bos",
                "D_phase2_model_visible_tokens",
                "revisit_epochs",
            ],
        )
        w.writeheader()
        for row in reporting["exposure_table"]:
            w.writerow({k: row[k] for k in w.fieldnames})
    dump(RESULTS / "a3_realized_shares.json", reporting["a3_realized_shares"])

    dump(
        RESULTS / "primary_contrasts.json",
        {
            "C_en": seal["contrasts"]["C_en"],
            "G_tl": seal["contrasts"]["G_tl"],
            "C_en_A3": seal["contrasts"]["C_en_A3"],
            "G_tl_A3": seal["contrasts"]["G_tl_A3"],
            "note": "One-seed d20. A3 is not mitigation. Tests do not alter C_en/G_tl.",
        },
    )

    (RESULTS / "README.md").write_text(
        """# Machine-readable P2 results

**P2 only.** Does not amend AsPredicted #306780 / ResearchBox 8735 / Hub `p1-fixed-d20-3x`.

Primary DVs are full-split `val_bpb_full` in `gate-u-seal.json` (test_read_count=0 at seal). In-loop trainer BPB is not confirmatory.

| File | Role |
|---|---|
| `sealed_val_table.csv` | A0/A1/A2/A3 English and Tagalog val BPB |
| `gate-u-seal.json` | Sealed table, contrasts, packing |
| `evaluation/a{1,2,3}_{english,tagalog}_val.json` | Six underlying Gate U full-val eval objects |
| `gate-v-test.json` | A2-only secondary tests |
| `test_access_log.json` | One authorized touch; two component reads |
| `gate_p0_val_baselines.json`, `p2-en0-d8_p0e_val.json`, `p2-en0-d20_p0e_val.json` | P0-E floors |
| `gate-q-a0.json`, `p2-en0-d20_a0_tagalog_val.json` | A0 freeze; official CUDA A0 Tagalog val |
| `gate-r-a1.json`, `gate-s-a2.json`, `gate-t-a3.json` | Branch lineage and checkpoint hashes |
| `gate-e-shards.json`, `a3_realized_shares.json`, `exposure_by_arm.csv` | Mix and exposure |
| `registered-reporting-q3-q8.json` | Q3–Q8 reconstruction (no test read) |
| `LOCK.sanitized.json` | Study lock without ResearchBox passcode |

Do not commit `*.pt`, `test.jsonl`, HOST SSH cards, or passcodes. CPU diagnostic A0 Tagalog 4.921200 is **not** official (CUDA 4.917650 is).
"""
    )

    # Hub documentation pack (no weights)
    hub_eval = HUB / "evaluation"
    hub_eval.mkdir(parents=True)
    dump(hub_eval / "full_validation_table.json", {"source": "gate-u-seal.json", "table_d20": table, "contrasts": seal["contrasts"]})
    dump(
        hub_eval / "primary_contrasts.json",
        {
            "C_EN": -0.07399123756067971,
            "G_TL": -3.883048460086431,
            "filed_C_EN": ">=0.01",
            "filed_G_TL": "<=-0.01",
            "C_EN_observed_as_filed": False,
            "G_TL_observed_as_filed": True,
            "one_seed": True,
        },
    )
    dump(hub_eval / "a3_tradeoff.json", reporting["a3_realized_shares"] | {"EN_A3_minus_A1": -0.18024170905276216, "TL_A3_minus_A1": -3.5258062502675505, "not_mitigation": True})
    v = json.loads((CARDS / "gate-v-test.json").read_text())
    dump(
        hub_eval / "a2_secondary_tests.json",
        {
            "arm": "A2",
            "english_test_bpb": v["english"]["bpb"],
            "tagalog_test_bpb": v["tagalog"]["bpb"],
            "does_not_alter_C_en_or_G_tl": True,
            "a1_tested": False,
            "a3_tested": False,
            "do_not_reuse_p11_test_bpb": 1.164768,
        },
    )

    sizes = {
        "a0/p2-en0-d20-model_005415.pt": (2663446486, "bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d"),
        "a1/p2-a1-extra-en-d20-model_000294.pt": (2663446486, "e2881049b194898203a954464bcb00939aa1d94b9b41131001ab705c2c92385d"),
        "a2/p2-a2-tagalog-d20-model_000294.pt": (2663446486, "2b01acf8fac0e8c783162582cbb384e8ce1c37795aae2f7dd4ae34c2a5c76026"),
        "a3/p2-a3-mix-d20-model_000294.pt": (2663446486, "d6c62bb793a57c7c23d98c5bd62ec36b41606234524f76855b4459d98c42b368"),
        "tokenizer.pkl": (414284, "946a04ef05e73be625f24ea5e88bfa4531546ae7d7238fbe1b0fd68df016ace6"),
        "token_bytes.pt": (132649, "5ae2ea1d214f2b7f98eeba606d461db62d04101e7a947a3201ec6bb2a7062d42"),
    }
    sums = ["# SHA-256 and byte sizes of the complete P2 release bundle.", "# Weights/tokenizer lines are pending Hub upload; hashes are sealed locally.", ""]
    for name, (nbytes, digest) in sizes.items():
        sums.append(f"{digest}  {nbytes}  {name}  PENDING_UPLOAD")
    (HUB / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n")

    dump(
        HUB / "RELEASE_MANIFEST.json",
        {
            "study": "NANOCHAT-FILIPINO-P2-EN-TL",
            "aspredicted": 306935,
            "hub": "pageman/nanochat-filipino-p2-en-then-tl",
            "status": "documentation_only_complete_checkpoint_bundle_pending",
            "run_id": "p2-20260817T150944Z-de99f8a",
            "nanochat_pin": "92d63d4e8bb4df75c3b71618f31ddde2378b2bcd",
            "does_not_amend_p11_hub": "pageman/nanochat-filipino-p1-fixed-d20-3x",
            "branches": {
                "A0": {"folder": "a0/", "role": "frozen EN0 d20 parent", "step": 5415, "sha256": sizes["a0/p2-en0-d20-model_005415.pt"][1], "parent": None},
                "A1": {"folder": "a1/", "role": "extra-English control", "step": 294, "sha256": sizes["a1/p2-a1-extra-en-d20-model_000294.pt"][1], "parent": "A0"},
                "A2": {"folder": "a2/", "role": "Tagalog continuation; only tested arm", "step": 294, "sha256": sizes["a2/p2-a2-tagalog-d20-model_000294.pt"][1], "parent": "A0"},
                "A3": {"folder": "a3/", "role": "50/50-document mix trade-off, not mitigation", "step": 294, "sha256": sizes["a3/p2-a3-mix-d20-model_000294.pt"][1], "parent": "A0"},
            },
            "fresh_optimizer_on_children": True,
            "optimizer_states_not_in_default_release": True,
        },
    )

    roles = {
        "a0": "Frozen English parent EN0 d20 (`model_005415.pt`). Not a chat model. Do not treat as P1.1.",
        "a1": "Extra-English matched-budget control from A0 (`model_000294.pt`). Never tested in P2.",
        "a2": "Tagalog continuation from A0. Only arm with authorized secondary test. Not P1.1 weights.",
        "a3": "50/50-document mix trade-off from A0. Not mitigation. Never tested in P2.",
    }
    for folder, text in roles.items():
        (HUB / folder).mkdir(exist_ok=True)
        (HUB / folder / "README.md").write_text(f"# P2 branch {folder.upper()}\n\n{text}\n\nDocumentation-only until the complete A0/A1/A2/A3 `.pt` bundle is uploaded together.\n")

    print(json.dumps({"results": str(RESULTS), "hub": str(HUB), "n_result_files": sum(1 for p in RESULTS.rglob("*") if p.is_file())}, indent=2))


if __name__ == "__main__":
    main()
