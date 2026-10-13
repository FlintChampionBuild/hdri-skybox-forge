"""Tonemap service: linear light <-> display-referred, exposure, filmic curves."""
from __future__ import annotations

import numpy as np

from hdri_forge.utils.logging import get_logger

log = get_logger(__name__)


class TonemapService:
    def __init__(self, cfg: "object") -> None:
        self._cfg = cfg

    def apply_exposure(self, linear: np.ndarray, ev: float) -> np.ndarray:
        """Scale linear-light radiance by 2**ev. No clipping — HDR stays HDR."""
        if ev == 0.0:
            return linear
        return linear * np.float32(2.0**ev)

    def filmic_aces(self, linear: np.ndarray) -> np.ndarray:
        """ACES approximation for preview thumbnails. NOT applied to exported EXR."""
        a, b, c, d, e = 2.51, 0.03, 2.43, 0.59, 0.14
        x = np.clip(linear, 0.0, None)
        return np.clip((x * (a * x + b)) / (x * (c * x + d) + e), 0.0, 1.0)