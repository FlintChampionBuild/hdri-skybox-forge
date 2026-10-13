"""Minimal system-tray shim for the desktop build. Windows-only."""
from __future__ import annotations

import sys

from hdri_forge.app.bootstrap import build_runtime
from hdri_forge.utils.logging import get_logger

log = get_logger(__name__)


def main() -> int:
    if sys.platform != "win32":
        log.error("tray.unsupported_platform", extra={"platform": sys.platform})
        return 2
    # pystray is an optional extra; the CLI is the primary surface.
    try:
        import pystray  # type: ignore[import-not-found]
    except ImportError:
        log.error("tray.missing_pystray", extra={"hint": "pip install hdri-skybox-forge[tray]"})
        return 3

    rt = build_runtime()
    log.info("tray.ready", extra={"adapter": rt.adapter.name})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())