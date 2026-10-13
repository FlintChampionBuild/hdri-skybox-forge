"""Config loading + typed view over default.toml / local.toml."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from hdri_forge.utils.paths import config_dir


@dataclass(slots=True, frozen=True)
class AppSection:
    log_level: str
    log_dir: str
    device: str
    precision: str
    tile_size: int


@dataclass(slots=True, frozen=True)
class ModelsSection:
    diffusion: str
    vae: str
    controlnet_sun: str
    default_lora_weight: float


@dataclass(slots=True, frozen=True)
class RenderSection:
    default_resolution: int
    faces: int
    projection: str
    sun_azimuth_deg: float
    sun_elevation_deg: float
    atmosphere_turbidity: float
    exposure_ev: float


@dataclass(slots=True, frozen=True)
class OutputSection:
    format: str
    half_float: bool
    write_sidecar_json: bool
    out_dir: str


@dataclass(slots=True, frozen=True)
class PerfSection:
    vram_budget_gb: int
    attention_slicing: bool
    vae_tiling: bool
    torch_compile: bool


@dataclass(slots=True, frozen=True)
class ForgeConfig:
    app: AppSection
    models: ModelsSection
    render: RenderSection
    output: OutputSection
    perf: PerfSection


def _merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    out = dict(base)
    for k, v in overlay.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(path: str | None = None) -> ForgeConfig:
    base_path = config_dir() / "default.toml"
    with base_path.open("rb") as fh:
        raw = tomllib.load(fh)

    local_path = Path(path) if path else config_dir() / "local.toml"
    if local_path.is_file():
        with local_path.open("rb") as fh:
            raw = _merge(raw, tomllib.load(fh))

    return ForgeConfig(
        app=AppSection(**raw["app"]),
        models=ModelsSection(**raw["models"]),
        render=RenderSection(**raw["render"]),
        output=OutputSection(**raw["output"]),
        perf=PerfSection(**raw["perf"]),
    )