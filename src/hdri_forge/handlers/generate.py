"""generate handler: SkyboxRequest -> SkyboxResult."""
from __future__ import annotations

from hdri_forge.app.bootstrap import ForgeRuntime
from hdri_forge.models.schemas import SkyboxRequest, SkyboxResult
from hdri_forge.utils.logging import get_logger

log = get_logger(__name__)


class GenerateHandler:
    def __init__(self, rt: ForgeRuntime) -> None:
        self._rt = rt

    def run(self, req: SkyboxRequest) -> SkyboxResult:
        log.info(
            "generate.start",
            extra={"res": req.resolution, "seed": req.seed, "projection": req.projection},
        )
        latents = self._rt.diffusion.render_equirect(req)
        toned = self._rt.tonemap.apply_exposure(latents, self._rt.config.render.exposure_ev)
        result = SkyboxResult(
            pixels=toned,
            resolution=req.resolution,
            projection=req.projection,
            seed=req.seed,
            prompt=req.prompt,
            metadata={"backend": self._rt.adapter.name, "forge": "0.6.2"},
        )
        log.info("generate.done", extra={"shape": getattr(toned, "shape", None)})
        return result