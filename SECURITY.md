# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | ✅        |
| 0.5.x   | ⚠️ security fixes only |
| < 0.5   | ❌        |

## Reporting a vulnerability

Do **not** open a public issue for security problems. Email
`security@hdri-skybox-forge.dev` with:

- Affected version and component (`services/`, `io/`, `adapters/`)
- Steps to reproduce
- Impact assessment (RCE, arbitrary file write, model deserialization, etc.)
- Any PoC files (keep them small)

We aim to acknowledge within 72 hours and ship a fix or mitigation within
14 days for confirmed high-severity issues.

## Threat model

`hdri-skybox-forge` loads user-supplied files in three places:

1. **Checkpoints / LoRAs** (`models/checkpoints/`, `models/loras/`) — loaded
   via `safetensors` only. `.ckpt` (pickle) loading is disabled by default;
   enabling it requires `--allow-pickle` and prints a loud warning. Pickle
   checkpoints are treated as untrusted code.
2. **Reference panoramas** (`.exr`, `.hdr`, `.png`, `.jpg`) — parsed by
   `io/` readers. Malformed headers are rejected; fuzzing corpus lives in
   `tests/fuzz/`.
3. **Preset TOML** (`config/*.toml`) — parsed with `tomllib`. No `eval`, no
   `exec`, no dynamic imports from config values.

## Out of scope

- GPU driver CVEs (report upstream)
- Denial-of-service via absurdly large prompts (rate-limit at the app layer)
- Anything requiring an attacker to already have local code execution