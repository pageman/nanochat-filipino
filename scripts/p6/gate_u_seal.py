#!/usr/bin/env python3
"""P6 Gate U: 12-cell validation matrix + lockboxed topology contrasts; seal hashes only."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / "vendor" / "nanochat"))

import torch  # noqa: E402
from evaluate_bpb import (  # noqa: E402
    PACKING,
    eval_model,
    pack_one_pass,
    parquet_texts,
    require_hash,
    sha256_file,
)
from nanochat.checkpoint_manager import load_model  # noqa: E402
from nanochat.common import compute_init  # noqa: E402
from nanochat.tokenizer import get_token_bytes  # noqa: E402
from p6_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    C1_DIR,
    C2_DIR,
    CHILD_ARMS,
    EXPECTED,
    LOCK_PATH,
    N_PHASE2,
    N_TL0,
    P6_RUN_ID,
    POLICY_A_TEST_ARM,
    RESEARCHBOX_ID,
    TOKENIZER_PKL_SHA,
    TOPOLOGY_ARMS,
    child_tag,
    mark_ledger,
    require_auth,
    seed_box,
    seed_card,
    seed_safe,
    sha256_bytes,
    tl0_tag,
    update_lock_gate,
    utc_now,
    write_json,
)


def cell_name(arm: str, lang: str) -> str:
    return f"{arm}_{lang}_val_bpb_full.json"


def write_cell(box: Path, name: str, val_bpb: float, detail: dict, tag: str, split: str) -> None:
    payload = {
        "gate": "U",
        "cell": name,
        "model_tag": tag,
        "split": split,
        "val_bpb_full": val_bpb,
        "evaluated_at_utc": utc_now(),
        "packing": PACKING,
        "test_read_count": 0,
        "detail": detail,
    }
    path = box / name
    path.write_text(json.dumps(payload, indent=2) + "\n")
    try:
        path.chmod(0o600)
    except OSError:
        pass


def eval_arm(tag: str, en_batches, tl_batches, token_bytes, en_pack, tl_pack):
    model, _tok, meta = load_model("base", torch.device("cuda"), phase="eval", model_tag=tag, step=N_PHASE2)
    assert meta["step"] == N_PHASE2
    en = eval_model(model, en_batches, token_bytes, en_pack, f"{tag}/english_val")
    tl = eval_model(model, tl_batches, token_bytes, tl_pack, f"{tag}/tagalog_val")
    del model
    torch.cuda.empty_cache()
    return en, tl


def main() -> int:
    seed = int(sys.argv[1])
    require_auth(seed_card(seed) / "gate-u-authorization.json", "U", {"seed": seed})
    # Prior gates
    for gate, arm in (("r", "c1"), ("s", "c2")):
        rec = seed_card(seed) / f"gate-{gate}-{arm}.json"
        if not rec.is_file() or json.loads(rec.read_text()).get("status") != "pass":
            raise SystemExit(f"Gate {gate.upper()}_{seed} not pass")
    for arm in TOPOLOGY_ARMS:
        rec = seed_card(seed) / f"gate-t-{arm}.json"
        if not rec.is_file() or json.loads(rec.read_text()).get("status") != "pass":
            raise SystemExit(f"Gate T_{seed} arm {arm} not pass")
    lock = json.loads(LOCK_PATH.read_text())
    if int(lock.get("test_access_count", {}).get(str(seed), 1)) != 0:
        raise SystemExit("test_access_count must be 0 before U")
    if lock.get("outcome_access_count", 1) != 0:
        raise SystemExit("outcome_access_count must be 0 before U")

    box = seed_box(seed)
    require_hash(BASE / "tokenizer" / "tokenizer.pkl", TOKENIZER_PKL_SHA, "tokenizer")
    require_hash(C1_DIR / "val.parquet", EXPECTED["c1_shards"]["val.parquet"], "tl_val")
    require_hash(C2_DIR / "val.parquet", EXPECTED["c2_shards"]["val.parquet"], "en_val")
    os.environ.setdefault("NANOCHAT_BASE_DIR", str(BASE))
    os.environ["P6_EVAL_QUIET"] = "1"
    compute_init("cuda")
    device = torch.device("cuda")
    _m, tokenizer, _meta = load_model("base", device, phase="eval", model_tag=child_tag(seed, "c1"), step=N_PHASE2)
    token_bytes = get_token_bytes(device=device)
    en_batches, en_pack = pack_one_pass(parquet_texts(C2_DIR / "val.parquet"), tokenizer, 8, 2048, device)
    tl_batches, tl_pack = pack_one_pass(parquet_texts(C1_DIR / "val.parquet"), tokenizer, 8, 2048, device)
    del _m
    torch.cuda.empty_cache()

    cells: dict[str, float] = {}
    for arm in CHILD_ARMS:
        tag = child_tag(seed, arm)
        print(f"Gate U_{seed} evaluating {tag} (scalars -> lockbox)", flush=True)
        en_d, tl_d = eval_arm(tag, en_batches, tl_batches, token_bytes, en_pack, tl_pack)
        write_cell(box, cell_name(arm, "en"), en_d["bpb"], en_d, tag, "english_val")
        write_cell(box, cell_name(arm, "tl"), tl_d["bpb"], tl_d, tag, "tagalog_val")
        cells[cell_name(arm, "en")] = float(en_d["bpb"])
        cells[cell_name(arm, "tl")] = float(tl_d["bpb"])

    print(f"Gate U_{seed} evaluating C0 English descriptive (scalars -> lockbox)", flush=True)
    model, _, _ = load_model("base", device, phase="eval", model_tag=tl0_tag(seed, 20), step=N_TL0)
    c0_en = eval_model(model, en_batches, token_bytes, en_pack, f"{tl0_tag(seed, 20)}/english_val")
    del model
    torch.cuda.empty_cache()
    write_cell(box, "c0_en_val_bpb_full.json", c0_en["bpb"], c0_en, tl0_tag(seed, 20), "english_val")

    required = [cell_name(a, lang) for a in CHILD_ARMS for lang in ("en", "tl")] + ["c0_en_val_bpb_full.json"]
    missing = [n for n in required if not (box / n).is_file()]
    if missing:
        raise SystemExit(f"incomplete U inventory: {missing}")

    # Frozen contrasts stay in lockbox only
    fine_tl = cells[cell_name(POLICY_A_TEST_ARM, "tl")]
    fine_en = cells[cell_name(POLICY_A_TEST_ARM, "en")]
    c2_tl = cells[cell_name("c2", "tl")]
    c1_en = cells[cell_name("c1", "en")]
    contrasts = {
        "schema": "p6-m-gate-u-contrasts-v1",
        "reference_topology": POLICY_A_TEST_ARM,
        "delta_vs_m_fine": {},
        "contextual_R_TL": {},
        "contextual_A_EN": {},
        "c0_en_descriptive_excluded_from_topology": True,
        "at_utc": utc_now(),
    }
    for tau in TOPOLOGY_ARMS:
        if tau == POLICY_A_TEST_ARM:
            continue
        contrasts["delta_vs_m_fine"][tau] = {
            "Delta_TL": cells[cell_name(tau, "tl")] - fine_tl,
            "Delta_EN": cells[cell_name(tau, "en")] - fine_en,
        }
    for tau in TOPOLOGY_ARMS:
        contrasts["contextual_R_TL"][tau] = cells[cell_name(tau, "tl")] - c2_tl
        contrasts["contextual_A_EN"][tau] = cells[cell_name(tau, "en")] - c1_en
    contrasts_path = box / f"p6-s{seed}-topology-contrasts.json"
    contrasts_path.write_text(json.dumps(contrasts, indent=2, sort_keys=True) + "\n")
    try:
        contrasts_path.chmod(0o600)
    except OSError:
        pass

    inventory = {n: sha256_file(box / n) for n in required}
    inventory["topology_contrasts"] = sha256_file(contrasts_path)
    seal = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "gate": "U",
        "seed": seed,
        "twelve_child_cells": True,
        "child_arms": list(CHILD_ARMS),
        "c0_en_descriptive": True,
        "contrasts_computed": True,
        "contrasts_in_lockbox_only": True,
        "policy_a_test_arm": POLICY_A_TEST_ARM,
        "test_access": 0,
        "inventory_sha256": inventory,
        "packing": PACKING,
        "seal_closed": True,
        "at_utc": utc_now(),
    }
    seal_path = box / f"p6-s{seed}-validation-seal.json"
    blob = json.dumps(seal, indent=2, sort_keys=True).encode()
    seal_path.write_bytes(blob)
    try:
        seal_path.chmod(0o600)
    except OSError:
        pass
    seal_sha = sha256_bytes(blob)
    write_json(
        seed_safe(seed) / "gate-u-status.json",
        {
            "seal_created": True,
            "seal_sha256": seal_sha,
            "test_access_count": 0,
            "contrasts_computed": True,
            "twelve_child_cells": True,
            "seed": seed,
        },
    )
    receipt = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "U",
        "seed": seed,
        "status": "pass",
        "at_utc": utc_now(),
        "gpu": True,
        "blinded": True,
        "p6_run_id": P6_RUN_ID,
        "seal_path": str(seal_path.relative_to(ROOT)),
        "seal_sha256": seal_sha,
        "test_access": 0,
        "contrasts_computed": True,
        "twelve_child_cells": True,
        "no_bpb_in_receipt": True,
        "next_gate": f"V_{seed}",
    }
    write_json(seed_card(seed) / "gate-u-seal.json", receipt)
    lock = json.loads(LOCK_PATH.read_text())
    lock.setdefault("test_access_count", {})[str(seed)] = 0
    write_json(LOCK_PATH, lock)
    update_lock_gate(f"U_{seed}", "pass", {"status": f"gate_u_{seed}_pass"})
    mark_ledger(f"U_{seed}", "pass", str((seed_card(seed) / "gate-u-seal.json").relative_to(ROOT)), f"V_{seed}")
    print(f"Gate U_{seed}: seal created; contrasts lockboxed; test_access=0", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
