# Lean / Mathlib pin for the revised MP paper

Toolchain: Lean 4.34.0-rc1 (`lean-toolchain`), matching mathlib4 `v4.34.0-rc1`.

This VM (and any non-Mac host) must **not** inherit
`ELAN_HOME=/Users/paulpajo/Projects/mathcode/.local/elan`. Use `./env.sh`.

```bash
. ./env.sh
lake update
lake exe cache get
lake build
```

- `KillingTower.lean` — Nat identities, **no** `import Mathlib`, no `sorry`.
- `MathlibOk.lean` — imports `Mathlib.Data.Nat.Basic` and kernel-checks the pin.

`.lake/` is gitignored. `lake-manifest.json` is committed after `lake update`.
