"""Adapter contract. Every backend implements this; services never touch torch directly."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import numpy as np


class ComputeAdapter(ABC):
    """A compute backend (CUDA, DirectML, CPU). Owns device placement + dtype."""

    name: str = "base"
    device: str = "cpu"

    @abstractmethod
    def build_diffusion_pipeline(
        self,
        *,
        checkpoint: str,
        vae: str,
        controlnet: str,
        tile_size: int,
        attention_slicing: bool,
        vae_tiling: bool,
    ) -> Any: ...

    @abstractmethod
    def run_pipeline(self, pipe: Any, **kwargs: Any) -> Any: ...

    @abstractmethod
    def to_linear_float32(self, tensor: Any) -> "np.ndarray": ...