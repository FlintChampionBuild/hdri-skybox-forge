"""Wire config -> adapters -> services -> handlers. Single composition root."""
from __future__ import annotations

from dataclasses import dataclass

from hdri_forge.adapters import select_adapter
from hdri_forge.adapters.base import ComputeAdapter
from hdri_forge.config import ForgeConfig, load_config
from hdri_forge.services.diffusion import DiffusionService
from hdri_forge.services.projection import ProjectionService
from hdri_forge.services.tonemap import TonemapService
from hdri_forge.utils.logging import get_logger

log = get_logger(__name__)


@dataclass(slots=True)
class ForgeRuntime:
    """Everything a handler needs, already constructed and ready."""

    config: ForgeConfig
    adapter: ComputeAdapter
    diffusion: DiffusionService
    projection: ProjectionService
    tonemap: TonemapService


def build_runtime(config_path: str | None = None) -> ForgeRuntime:
    cfg = load_config(config_path)
    adapter = select_adapter(cfg.app.device, cfg.app.precision, cfg.perf.vram_budget_gb)
    log.info("runtime.adapter", extra={"backend": adapter.name, "device": adapter.device})

    diffusion = DiffusionService(cfg, adapter)
    projection = ProjectionService(cfg)
    tonemap = TonemapService(cfg)

    return ForgeRuntime(
        config=cfg,
        adapter=adapter,
        diffusion=diffusion,
        projection=projection,
        tonemap=tonemap,
    )