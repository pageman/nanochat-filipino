/-
  Mathlib smoke test for this pin (`lean-toolchain` = v4.34.0-rc1).
  KillingTower.lean remains Mathlib-free.
-/
import Mathlib.Data.Nat.Basic

theorem mathlib_nat_add_comm (n m : Nat) : n + m = m + n :=
  Nat.add_comm n m
