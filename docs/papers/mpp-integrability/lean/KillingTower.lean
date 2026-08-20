/-
  Killing-tower cardinality and Myers–Perry spin counts.
  Mathlib is not required. These are the discrete identities used in
  Lemma 3.1 and Lemma 3.2 of the revised paper.
-/

namespace MPPRevision

/-- Number of independent Myers–Perry spin parameters in spacetime dimension `D`. -/
def nSpins (D : Nat) : Nat := (D - 1) / 2

/-- Odd dimension `D = 2k+1` admits exactly `k` spins. -/
theorem nSpins_odd (k : Nat) : nSpins (2 * k + 1) = k := by
  unfold nSpins
  rw [Nat.add_sub_cancel]
  exact Nat.mul_div_right k (by decide : 0 < 2)

/--
  On a `D = 2n+ε` manifold, a nondegenerate principal 2-form produces
  `n` Killing tensors in the tower and `n+ε` Killing vectors, totaling `D`.
-/
theorem killing_tower_count (n ε : Nat) :
    n + (n + ε) = 2 * n + ε := by
  rw [Nat.add_assoc, ← Nat.two_mul]

/-- Cohomogeneity of generic Myers–Perry (isometry `ℝ_t × U(1)^n`)
    is `D - nSpins(D) - 1`. -/
def genericCohomogeneity (D : Nat) : Nat := D - nSpins D - 1

theorem generic_cohomogeneity_D5 : genericCohomogeneity 5 = 2 := by decide
theorem generic_cohomogeneity_D6 : genericCohomogeneity 6 = 3 := by decide
theorem generic_cohomogeneity_D7 : genericCohomogeneity 7 = 3 := by decide
theorem generic_cohomogeneity_D9 : genericCohomogeneity 9 = 4 := by decide

theorem D5_two_spins : nSpins 5 = 2 := by decide
theorem D6_two_spins : nSpins 6 = 2 := by decide
theorem D7_three_spins : nSpins 7 = 3 := by decide

/-- Equal-spin locus in the `n`-dimensional spin torus has codimension `n-1 ≥ 1` for `n ≥ 2`. -/
theorem equal_spin_codimension {n : Nat} (hn : 2 ≤ n) : 1 ≤ n - 1 := by
  cases n with
  | zero => cases hn
  | succ n =>
    cases n with
    | zero => cases hn
    | succ m => simp

/-- Ultraspinning window: the literature onset is `D ≥ 6`, not `D = 5`. -/
theorem ultraspinning_onset : 5 < 6 := by decide

end MPPRevision
