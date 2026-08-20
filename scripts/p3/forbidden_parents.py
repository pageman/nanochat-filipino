#!/usr/bin/env python3
"""P3 parent-SHA reject list. Confirmatory children MUST NOT load these files."""

from __future__ import annotations

FORBIDDEN_PARENT_SHA256 = {
    # P1.1 d20 model_000294.pt
    "9e30fff3d6effc7c71af92e8488f9375a5d70cf1962ba371bee0e639836dde38",
    # P2 A0 EN0 d20
    "bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d",
}


def reject_parent_sha256(sha256: str) -> None:
    digest = sha256.lower().strip()
    if digest in FORBIDDEN_PARENT_SHA256:
        raise SystemExit(f"P3 forbids P1.1/P2 parent SHA256 {digest}")
