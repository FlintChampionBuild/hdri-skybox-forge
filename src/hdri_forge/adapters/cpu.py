"""CPU adapter — slow but always available. Used for CI and headless servers."""
from __future__ import annotations

from typing import Any

import numpy as np

from hdri_forge.adapters.base import ComputeAdapter
from hdri_forge.utils.logging import get_logger

log = get_logger(__name__)


class CpuAdapter(ComputeAdapter):
    name = "cpu"

    def __init__(self, *, precision: str) -> None:
        self.device = "cpu"
        self.precision = "fp32"  # CPU fp16 is slower than fp32 on x86
        log.info("adapter.cpu_init")

    def build_diffusion_pipeline(self,