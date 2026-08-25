#!/usr/bin/env python3
"""P6 Gate V: one Policy A M-fine restricted-test event. Scalars stay in seed lockbox."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / "vendor" / "nanochat"))

from evaluate_bpb import PACKING, STRIDE, eval_model, jsonl_texts, pack_one_pass, require_hash, sha256_file  # noqa: E402
from nanochat.checkpoint_manager import load_model  # noqa: E402
from nanochat.common import compute_init  # noqa: E402
from nanochat.tokenizer import get_token_bytes  # noqa: E402
from p6_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    EN_TEST_JSONL,
    EXPECTED,
    LOCK_PATH,
    N_PHASE2,
    P6_RUN_ID,
    POLICY_A_TEST_ARM,
    RESEARCHBOX_ID,
    TL_TEST_JSONL,
    child_tag,
    mark_ledger,
    require_auth,
    seed_box,
    seed_card,
    seed_safe,
    update_lock_gate,
    utc_now,
    write_json,
)


def run_one(seed: int, which: str, ckpt_sha: str) -> dict:
    if os.environ.get("GATE_V_AUTHORIZED") != "1":
        raise SystemExit("set GATE_V_AUTHORIZED=1")
    box = seed_box(seed)
    seal = box / f"p6-s{seed}-validation-seal.json"
    if not seal.is_file():
        raise SystemExit("missing U seal")
    seal_row = json.loads(seal.read_text())
    if seal_row.get("test_access", 1) != 0:
        raise SystemExit("seal test_access must be 0")
    if seal_row.get("policy_a_test_arm") != POLICY_A_TEST_ARM:
        raise SystemExit("seal policy_a_test_arm mismatch")
    test_path = EN_TEST_JSONL if which == "english" else TL_TEST_JSONL
    expected = EXPECTED["en_test_jsonl"] if which == "english" else EXPECTED["tl_test_jsonl"]
    require_hash(test_path, expected, which + "_test")
    compute_init("cuda")
    import torch

    device = torch.device("cuda")
    tag = child_tag(seed, POLICY_A_TEST_ARM)
    model, tokenizer, meta = load_model("base", device, phase="eval", model_tag=tag, step=N_PHASE2)
    if meta.get("step") != N_PHASE2:
        raise SystemExit("unexpected step")
    if sha256_file(BASE / "base_checkpoints" / tag / f"model_{N_PHASE2:06d}.pt") != ckpt_sha:
        raise SystemExit(f"{POLICY_A_TEST_ARM} SHA mismatch")
    token_bytes = get_token_bytes(device=device)
    batches, pack = pack_one_pass(jsonl_texts(test_path), tokenizer, 8, 2048, device)
    out = eval_model(model, batches, token_bytes, pack, f"{tag}/{which}_test")
    del model
    torch.cuda.empty_cache()
    event = {
        "at_utc": utc_now(),
        "seed": seed,
        "component": which,
        "arm": POLICY_A_TEST_ARM,
        "model_tag": tag,
        "checkpoint_sha256": ckpt_sha,
        "test_path": str(test_path.relative_to(ROOT)),
        "bpb": out["bpb"],
        "total_nats": out["total_nats"],
        "total_bytes": out["total_bytes"],
        "packing": PACKING,
        "stride": STRIDE,
        "does_not_alter_sealed_contrasts": True,
        "secondary_excluded_from_topology": True,
    }
    lock_path = box / f"gate-v-{POLICY_A_TEST_ARM}-{which}-test.json"
    lock_path.write_text(json.dumps(event, indent=2) + "\n")
    try:
        lock_path.chmod(0o600)
    except OSError:
        pass
    return event


def main() -> int:
    seed = int(sys.argv[1])
    require_auth(seed_card(seed) / "gate-v-authorization.json", "V", {"seed": seed})
    t_rec = json.loads((seed_card(seed) / f"gate-t-{POLICY_A_TEST_ARM}.json").read_text())
    u_rec = json.loads((seed_card(seed) / "gate-u-seal.json").read_text())
    if t_rec.get("status") != "pass" or u_rec.get("status") != "pass":
        raise SystemExit("T(m-fine)/U must pass")
    # Append ledger BEFORE launch (interrupt-safe one-touch)
    ledger = seed_card(seed) / "gate-v-test-access-ledger.jsonl"
    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(
            json.dumps(
                {
                    "at_utc": utc_now(),
                    "seed": seed,
                    "arm": POLICY_A_TEST_ARM,
                    "event": "authorized_touch_begin",
                    "policy": "one_m_fine_only_restricted_test_after_validation_seal",
                }
            )
            + "\n"
        )
    os.environ["GATE_V_AUTHORIZED"] = "1"
    os.environ.setdefault("NANOCHAT_BASE_DIR", str(BASE))
    os.environ["P6_EVAL_QUIET"] = "1"
    events = [
        run_one(seed, "english", t_rec["checkpoint_sha256"]),
        run_one(seed, "tagalog", t_rec["checkpoint_sha256"]),
    ]
    box = seed_box(seed)
    summary = {
        "gate": "V",
        "seed": seed,
        "arm": POLICY_A_TEST_ARM,
        "authorized_touches": 1,
        "component_evaluations": 2,
        "checkpoint_sha256": t_rec["checkpoint_sha256"],
        "at_utc": utc_now(),
        "test_access": 1,
        "secondary_excluded_from_topology": True,
        "events": events,
    }
    (box / f"gate-v-s{seed}-test.json").write_text(json.dumps(summary, indent=2) + "\n")
    try:
        (box / f"gate-v-s{seed}-test.json").chmod(0o600)
    except OSError:
        pass
    write_json(
        seed_safe(seed) / "gate-v-status.json",
        {
            "one_authorized_m_fine_only_test_event_completed": True,
            "test_access_count": 1,
            "component_evaluations": 2,
            "arm": POLICY_A_TEST_ARM,
            "seed": seed,
        },
    )
    receipt = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "V",
        "seed": seed,
        "status": "pass",
        "at_utc": utc_now(),
        "p6_run_id": P6_RUN_ID,
        "gpu": True,
        "blinded": True,
        "arm": POLICY_A_TEST_ARM,
        "authorized_touches": 1,
        "component_evaluations": 2,
        "test_access": 1,
        "no_bpb_in_receipt": True,
        "next_gate": "X",
    }
    write_json(seed_card(seed) / "gate-v-test.json", receipt)
    lock = json.loads(LOCK_PATH.read_text())
    lock.setdefault("test_access_count", {})[str(seed)] = 1
    write_json(LOCK_PATH, lock)
    update_lock_gate(f"V_{seed}", "pass", {"status": f"gate_v_{seed}_pass"})
    mark_ledger(f"V_{seed}", "pass", str((seed_card(seed) / "gate-v-test.json").relative_to(ROOT)), "X")
    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"at_utc": utc_now(), "seed": seed, "event": "authorized_touch_complete", "test_access": 1}) + "\n")
    print(f"one authorized {POLICY_A_TEST_ARM}-only test event completed for seed {seed}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
