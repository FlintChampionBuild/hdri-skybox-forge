"""CUDA adapter — the fast path. Requires torch+cuda and an NVIDIA GPU."""
from __future__ import annotations

from typing import Any

from hdri_forge.adapters.base import ComputeAdapter
from hdri_forge.utils.logging import get_logger

log = get_logger(__name__)


class CudaAdapter(ComputeAdapter):
    name = "cuda"

    def __init__(self, *, precision: str, vram_budget_gb: int) -> None:
        import torch

        if not torch.cuda.is_available():
            raise RuntimeError("torch.cuda.is_available() is False")
        self._torch = torch
        self._dtype = {"fp16": torch.float16, "bf16": torch.bfloat16, "fp32": torch.float32}[precision]
        self.device = "cuda"
        self.vram_budget_gb = vram_budget_gb
        log.info(
            "adapter.cuda_init",
            extra={"gpu": torch.cuda.get_device_name(0), "dtype": precision},
        )

    def build_diffusion_pipeline(self, *, checkpoint: str, vae: str, controlnet: str, tile_size: int, attention_slicing: bool, vae_tiling: bool) -> Any:
        from diffusers import StableDiffusionXLPipeline

        pipe = StableDiffusionXLPipeline.from_single_file(checkpoint, torch_dtype=self._dtype)
        pipe.to(self.device)
        if attention_slicing:
            pipe.enable_attention_slicing()
        if vae_tiling:
            pipe.enable_vae_tiling()
        return pipe

    def run_pipeline(self, pipe: Any, **kwargs: Any) -> Any:
        return pipe(
            prompt=kwargs["prompt"],
            negative_prompt=kwargs["negative_prompt"],
            width=kwargs["width"],
            height=kwargs["height"],
            num_inference_steps=32,
            guidance_scale=6.5,
            output_type="latent",
        ).images

    def to_linear_float32(self, tensor: Any) -> Any:
        return tensor.detach().float().cpu().numpy()