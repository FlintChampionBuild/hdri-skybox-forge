"""Typer CLI — thin. Parses args, builds runtime, calls handlers."""
from __future__ import annotations

import typer
from rich.console import Console

from hdri_forge.app.bootstrap import build_runtime
from hdri_forge.handlers.generate import GenerateHandler
from hdri_forge.handlers.export import ExportHandler
from hdri_forge.models.schemas import SkyboxRequest

app = typer.Typer(add_completion=False, help="AI skybox / HDRI generator")
console = Console()


@app.command()
def generate(
    prompt: str = typer.Argument(..., help="Scene description, e.g. 'stormy dusk over basalt cliffs'"),
    out: str = typer.Option("out/sky.exr", "--out", "-o"),
    resolution: int = typer.Option(4096, "--res"),
    seed: int = typer.Option(6767, "--seed"),
    projection: str = typer.Option("equirect", "--projection"),
    config: str | None = typer.Option(None, "--config"),
) -> None:
    """Generate an HDRI from a text prompt."""
    rt = build_runtime(config)
    req = SkyboxRequest(
        prompt=prompt,
        resolution=resolution,
        seed=seed,
        projection=projection,  # type: ignore[arg-type]
    )
    result = GenerateHandler(rt).run(req)
    ExportHandler(rt).run(result, out)
    console.print(f"[green]wrote[/green] {out}  ({result.resolution}px, seed={result.seed})")


def main() -> None:
    app()