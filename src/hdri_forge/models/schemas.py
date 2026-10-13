"""Boundary types. Handlers speak these; services speak tensors."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Projection = Literal["equirect", "cubemap", "fisheye", "latlong"]
OutputFormat = Literal["exr", "hdr", "png16", "ktx2", "dds"]


@dataclass(slots=True, frozen=True)
class SkyboxRequest:
    prompt: str
    resolution: int = 4096
    seed: int = 6767
    projection: Projection = "equirect"
    sun_azimuth_deg: float | None = None
    sun_elevation_deg: float | None = None
    lora_weight: float | None = None
    negative_prompt: str = "text, watermark, ui, people, ground plane"


@dataclass(slots=True, frozen=True)
class SkyboxResult:
    """In-memory HDR panorama: linear-light float32, shape (H, W, 3)."""

    pixels: "object"  # numpy.ndarray — typed loosely to avoid a hard numpy import at model layer
    resolution: int
    projection: Projection
    seed: int
    prompt: str
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class CubemapResult:
    faces: tuple["object", ...]  # six (S, S, 3) float32 arrays, +X -X +Y -Y +Z -Z
    face_size: int
    seed: int
    metadata: dict[str, str] = field(default_factory=dict)