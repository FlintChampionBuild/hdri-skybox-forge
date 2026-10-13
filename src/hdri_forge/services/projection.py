"""Projection service: equirect <-> cubemap / fisheye / latlong."""
from __future__ import annotations

import numpy as np

from hdri_forge.utils.logging import get_logger

log = get_logger(__name__)


class ProjectionService:
    def __init__(self, cfg: "object") -> None:
        self._cfg = cfg

    def equirect_to_cubemap(self, panorama: np.ndarray, face_size: int, faces: int = 6) -> tuple[np.ndarray, ...]:
        """Reproject an equirect (H, W, 3) panorama into `faces` square faces.

        Uses a per-pixel direction lookup; O(face_size^2 * faces) and
        allocation-heavy, so results are memoized by the caller if reused.
        """
        if faces != 6:
            raise ValueError(f"cubemap faces must be 6, got {faces}")
        h, w = panorama.shape[:2]
        # Face order: +X, -X, +Y, -Y, +Z, -Z (matches DDS / KTX2 convention).
        basis = np.array(
            [
                [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                [[-1, 0, 0], [0, 1, 0], [0, 0, -1]],
                [[1, 0, 0], [0, 0, 1], [0, -1, 0]],
                [[1, 0, 0], [0, 0, -1], [0, 1, 0]],
                [[1, 0, 0], [0, 1, 0], [0, 0, -1]],
                [[-1, 0, 0], [0, 1, 0], [0, 0, 1]],
            ],
            dtype=np.float32,
        )
        out = []
        lin = np.linspace(-1.0, 1.0, face_size, dtype=np.float32)
        uu, vv = np.meshgrid(lin, lin[::-1])
        for f in range(faces):
            r, u, b = basis[f][0], basis[f][1], basis[f][2]
            dirs = r[None, None, :] * uu[..., None] + u[None, None, :] * vv[..., None] + b[None, None, :]
            dirs /= np.linalg.norm(dirs, axis=-1, keepdims=True)
            lon = np.arctan2(dirs[..., 0], dirs[..., 2])
            lat = np.arcsin(np.clip(dirs[..., 1], -1.0, 1.0))
            sx = ((lon / (2 * np.pi) + 0.5) * (w - 1)).astype(np.int32)
            sy = ((0.5 - lat / np.pi) * (h - 1)).astype(np.int32)
            out.append(panorama[sy, sx])
        log.debug("projection.cubemap_done", extra={"face_size": face_size})
        return tuple(out)