# Host-offer classification — NVIDIA DGX Spark for official H/I

- Date (UTC): 2026-08-16 (written after the offer document was received, before any Spark command)
- Operator: Paul Pajo
- Offer file: `/Users/paulpajo/Downloads/dgx_spark_gate_h_i_assessment.md`
- Classification: **conditionally eligible CUDA host offer, not yet named**
- `gpu_host_for_H_I`: still **null** until Spark-local CUDA preflight passes

## Frozen statement affected

`manifests/execution_host.json` still records this Mac for A–G and leaves official H/I unnamed. A DGX Spark may become that named host only after architecture-aware CUDA preflight.

## Decision adopted from the offer

The Spark is a real NVIDIA CUDA host (GB10 / Blackwell, 128 GB unified memory, Arm64). It is **not** automatically official. ARM64 + `torch==2.9.1` + `pytorch-cu128` must be proven on the machine. A failed install, CPU fallback, or code change to fit the device classifies the Spark as `blocked`.

Mac MPS jobs remain non-confirmatory.

## What this offer does not authorize

- Marking Gate H `pass` from the Mac
- Running `p1-fixed-d*-3x` before official H
- Shrinking `T=2048`, dropping d20, or changing `B=65536`
- Passing `--target-param-data-ratio=-1`
- Running `python -m nanochat.dataset`
- Reading test BPB
- Putting the ResearchBox passcode on the Spark or in the transfer zip
