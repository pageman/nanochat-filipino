# Execution-only — API key rotation is now due

- Date (UTC): 2026-08-16
- Operator: Paul Pajo
- Supersedes the deferral in `2026-08-16-api-key-rotation-deferred.md` for timing only

## Decision

Gate I seed-0 training and Gate J confirmatory eval are finished. The earlier deferral is no longer in force. Rotate the exposed Runpod API key in the Runpod console, then update `~/.runpod/config.toml` (mode 600) and any MCP Bearer. Do not paste the new key into chat, Colab, or a zip.

This agent cannot rotate the account key without locking the running pod mid-job. Extra-seed / `D_1x` close-out may finish on the current key; rotate as soon as that job ends or from a second key if the console allows overlap.

This does not change depths, `T`, `B`, `N`, ratios, tokenizer, corpus, or `D*`.
