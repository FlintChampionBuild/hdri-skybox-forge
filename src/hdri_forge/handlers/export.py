"""export handler: SkyboxResult -> file on disk."""
from __future__ import annotations

from pathlib import Path

from hdri_forge.app.bootstrap import ForgeRuntime
from hdri_forge.io import get_writer
from hdri_forge.models.schemas import SkyboxResult
from hdri_forge.utils.logging import get_logger

log = get_logger(__name__)


class ExportHandler:
    def __init__(self, rt: ForgeRuntime) -> None:
        self._rt = rt

    def run(self, result: SkyboxResult, out_path: str) -> Path:
        dest = Path(out_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        writer = get_writer(self._rt.config.output, dest.suffix)
        writer.write(result, dest)
        log.info("export.written", extra={"path": str(dest)})
        return dest