# P6-M lockout-resistant architecture

Authority: filed AsPredicted #307969, addendum SHA
`df49664809ada69d23dcd2c799e75b30f0fdb9afd7aee12b071ac24ef2f81082`, LOCK.json.

## Principle

Never let a gate-critical checkpoint exist in only one place that is physically
pinned to a single host. After every gate pass, push the minimum viable resume
kit to a second location you control independently.

## P5 failure mode (Gate S)

A pod `/workspace` volume is host-pinned. When that host has no free GPUs,
start fails with `500: There are not enough free GPUs on the host machine`.
You cannot migrate the volume; you can only poll or reprovision elsewhere with
a portable resume kit.

## Two-tier state

| Tier | Location | Contents |
|---|---|---|
| 1 | Pod workspace | Full training state (optimizer, scheduler, all checkpoints). Treat as host-ephemeral for A40 work. |
| 2 | Portable resume kit | Latest checkpoint `.pt`, `tokenizer.pkl`, `token_bytes.pt`, run scripts + env hashes, `LOCK.json` / gate ledger. |

## 200 GB network volume

- Id: `3xuadadrph`
- Name: `p6-m-archive-200gb`
- Size: 200 GB STANDARD
- Datacenter: `CA-MTL-3`

**200 GB is storage, not VRAM.** A40 VRAM remains 48 GB.

### Live-mount constraint

Observed A40 capacity was in datacenters that did not advertise network-volume
types (e.g. CA-MTL-1). A volume in CA-MTL-3 cannot mount on an A40 pod in a
different datacenter. Until A40 appears in a volume-capable DC colocated with
`3xuadadrph`, Tier-2 **local** sync (Mac / off-host copy) is mandatory for live
recovery; the network volume is archival / future-colocation.

## Operational invariants

1. After every gate pass (Q–V), sync the resume kit off the pod host.
2. Training launch must accept `--resume-from` for cold start on a new pod.
3. Write LOCK / gate ledger into Tier 2 immediately after each gate pass.
4. Alert after repeated pod-start 500s; offer reprovision instead of silent polling.
5. Do not delete the only copy of a gate-critical checkpoint without a verified Tier-2 receipt.
