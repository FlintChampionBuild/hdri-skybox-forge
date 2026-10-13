"""DirectML adapter — AMD / Intel GPU path on Windows via torch-directml."""
from __future__ import annotations

from typing import Any

from hdri_forge.adapters.base import ComputeAdapter
from hdri_forge.utils.logging import get_logger

log = get_logger(__name__)


class DirectMLAdapter(ComputeAdapter):
    name = "directml"

    def __init__(self, *, precision: str) -> None:
        import torch_directml  # type: ignore[import-not-found]

        self._dml = torch_directml
        self.device = f"privateuseone:0"
        self._dtype = "float16" if precision == "fp16" else "float32"
        log.info("adapter.directml_init", extra={"device": self.device})

    def build_diffusion_pipeline(self, *, checkpoint: str, vae: str, controlnet: str, tile_size: int, attention_slicing: bool, vae_tiling: bool) -> Any:
        raise NotImplementedError(
            "DirectML pipeline wiring is tracked in issue #212; use --device cpu as a fallback."
        )

    def run_pipeline(self, pipe: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    def to_linear_float32(self, tensor: Any) -> Any:
        return tensor.cpu().numpy()