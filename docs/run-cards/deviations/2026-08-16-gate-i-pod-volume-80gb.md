# Execution-only — Gate I uses an 80 GB pod volume, not a network volume

- Date (UTC): 2026-08-16
- Operator: Paul Pajo

## Why

A40 Secure stock is CA-MTL-1 / EU-SE-1. Those data centers do not offer Runpod network volumes. The checklist forbids a 20 GB volume and asks for 80–100 GB persistent capacity.

## Plan

Create the Gate I Pod with `--volume-in-gb 80` mounted at `/workspace`. After each finished depth, export and hash the final checkpoint bundle to this Mac. If the Pod dies, that depth is restarted; mid-run checkpoints are diagnostic only.

This does not change `T`, `B`, `N`, ratios, depths, or `D*`.
