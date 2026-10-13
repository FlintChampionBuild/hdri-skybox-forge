# Contributing to hdri-skybox-forge

Thanks for wanting to push pixels. This repo generates equirectangular HDRIs
and 6-face cubemaps from text prompts, reference panoramas, or a fixed sun
vector — for game engines, DCC tools, and real-time renderers.

## Ground rules

- **One service, one job.** Handlers stay thin (parse → call → serialize).
  Business logic lives in `src/hdri_forge/services/`. If you're writing an
  `if` about GPU vs CPU in a handler, it belongs in an adapter.
- **No raw tensor shapes in handlers.** Convert to `SkyboxRequest` /
  `SkyboxResult` dataclasses at the boundary.
- **Every new pipeline stage gets a test** under `tests/`. Mock the diffusion
  backend; never call a real checkpoint in CI.
- **Determinism matters.** Anything that touches the RNG must accept a
  `seed: int` and thread it through `utils/rng.py`.

## Layout

```
src/hdri_forge/
  app/          # bootstrap, CLI, tray entry
  handlers/     # thin request/response layer
  services/     # business logic (diffusion, tonemap, projection)
  models/       # dataclasses + pydantic schemas
  adapters/     # cuda / cpu / directml platform shims
  io/           # exr, hdr, ktx2, dds writers
  utils/        # rng, logging, paths
config/         # default + preset toml
tests/          # pytest
```

## Dev setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev,cuda]
pytest -q
```

## Style

- `ruff` + `black`, line length 100.
- Type hints on every public function. `mypy --strict` on `services/`.
- Log with `utils.logging.get_logger(__name__)`, never `print`.

## PR checklist

- [ ] Tests pass locally (`pytest -q`)
- [ ] `ruff check src tests` clean
- [ ] New config keys documented in `config/default.toml`
- [ ] No checkpoints, no `.exr`/`.hdr` blobs committed
- [ ] PR description says *why*, not just *what*

## Reporting bugs

Include: OS build, GPU + driver, Python version, the exact prompt or input
panorama hash, and the full `logs/forge.log` tail. Repro beats description.