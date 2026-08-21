import Lake
open Lake DSL

package «mpp_revision» where
  -- Mathlib is available to this package. KillingTower.lean itself
  -- does not import it: the identities are Nat-only.
  leanOptions := #[
    ⟨`autoImplicit, false⟩,
    ⟨`relaxedAutoImplicit, false⟩
  ]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.34.0-rc1"

@[default_target]
lean_lib «KillingTower» where
  globs := #[.one `KillingTower]

/-- Smoke-check that Mathlib itself kernel-checks in this pin. -/
lean_lib «MathlibOk» where
  globs := #[.one `MathlibOk]
