"""Platform adapters — pick the right compute backend for this machine."""
from __future__ import annotations

from hdri_forge.adapters.base import ComputeAdapter
from hdri_forge.adapters.cpu import CpuAdapter
from hdri_forge.utils.logging import get_logger

log = get_logger(__name__)


def select_adapter(device: str, precision: str, vram_budget_gb: int) -> ComputeAdapter:
    """Return a concrete adapter. `device='auto'` probes CUDA -> DirectML -> CPU."""
    if device == "cpu":
        return CpuAdapter(precision=precision)
    if device == "cuda":
        from hdri_forge.adapters.cuda import CudaAdapter

        return CudaAdapter(precision=precision, vram_budget_gb=vram_budget_gb)
    if device == "directml":
        from hdri_forge.adapters.directml import DirectMLAdapter

        return DirectMLAdapter(precision=precision)

    # auto
    try:
        from hdri_forge.adapters.cuda import CudaAdapter

        return CudaAdapter(precision=precision, vram_budget_gb=vram_budget_gb)
    except Exception as exc:  # noqa: BLE001 — probe failure is expected on non-NVIDIA boxes
        log.info("adapter.cuda_unavailable", extra={"reason": str(exc)})
    try:
        from hdri_forge.adapters.directml import DirectMLAdapter

        return DirectMLAdapter(precision=precision)
    except Exception as exc:  # noqa: BLE001
        log.info("adapter.directml_unavailable", extra={"reason": str(exc)})
    return CpuAdapter(precision="fp32")