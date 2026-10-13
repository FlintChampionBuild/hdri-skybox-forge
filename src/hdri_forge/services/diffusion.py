"""Diffusion service. Owns the pipeline; hands raw linear-light panoramas back."""
from __future__ import annotations

from typing import TYPE_CHECKING

from hdri_forge.utils.logging import get_logger
from hdri_forge.utils.rng import seeded

if TYPE_CHECKING:
    import numpy as np

    from hdri_forge.adapters.base import ComputeAdapter
    from hdri_forge.config import ForgeConfig
    from hdri_forge.models.schemas import SkyboxRequest

log = get_logger(__name__)


class DiffusionService:
    """Wraps a text-to-panorama diffusion pipeline.

    The pipeline is lazily constructed on first render so cold-start CLI
    invocations (`hdri-forge --help`) don't pay the checkpoint-load tax.
    """

    def __init__(self, cfg: ForgeConfig, adapter: ComputeAdapter) -> None:
        self._cfg = cfg
        self._adapter = adapter
        self._pipe = None  # built on first use

    def _ensure_pipeline(self) -> None:
        if self._pipe is not None:
            return
        self._pipe = self._adapter.build_diffusion_pipeline(
            checkpoint=self._cfg.models.diffusion,
            vae=self._cfg.models.vae,
            controlnet=self._cfg.models.controlnet_sun,
            tile_size=self._cfg.app.tile_size,
            attention_slicing=self._cfg.perf.attention_slicing,
            vae_tiling=self._cfg.perf.vae_tiling,
        )
        log.info("diffusion.pipeline_ready")

    def render_equirect(self, req: SkyboxRequest) -> "np.ndarray":
        self._ensure_pipeline()
        height = req.resolution // 2
        with seeded(req.seed):
            latents = self._adapter.run_pipeline(
                self._pipe,
                prompt=req.prompt,
                negative_prompt=req.negative_prompt,
                width=req.resolution,
                height=height,
                lora_weight=req.lora_weight or self._cfg.models.default_lora_weight,
                sun_azimuth=req.sun_azimuth_deg or self._cfg.render.sun_azimuth_deg,
                sun_elevation=req.sun_elevation_deg or self._cfg.render.sun_elevation_deg,
            )
        return self._adapter.to_linear_float32(latents)