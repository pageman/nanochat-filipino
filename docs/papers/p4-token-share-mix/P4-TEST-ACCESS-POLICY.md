# P4 test-access policy

**Purpose:** Bind the secondary holdout rule.  
**Acceptance:** Policy A or B signed in PDF before Gate A.

## Policy A (recommended)

1. C1 and C2 are **never** evaluated on P4 test files.  
2. C3 is evaluated **once** on named EN WT103-raw test (`2bccabc0…`) and TL P1.1 `test.jsonl` (`3bd19345…`) as a **single authorized event**.  
3. Log `test_access_count=1` even though two component evals.  
4. Lockbox until Gate X.  
5. Descriptive secondary; not arm selection; not a test-set \(R_{\mathrm{TL}}\)/\(A_{\mathrm{EN}}\).  
6. Do not cite P1.1 `1.164768` or P2/P3 Gate V as P4.

## Policy B

No test event. Validation-only closeout. `test_access_count` remains 0.

## Policy C

Prohibited unless the PDF fully justifies testing C1 or C2 **before filing**.

## Hard stops

Test before U seal; C1/C2 test files present; second “peek”; printing test BPB before X.
