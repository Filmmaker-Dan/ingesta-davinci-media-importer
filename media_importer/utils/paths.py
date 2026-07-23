"""Path helpers for Ingesta install and import."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def normalize_path(path: str) -> str:
    """Expand user home and resolve to an absolute normalized path string."""
    raw = str(path).strip().strip('"')
    if not raw:
        return ""
    try:
        return str(Path(raw).expanduser().resolve())
    except OSError:
        return str(Path(raw).expanduser())


def plugins_dir() -> Path:
    if sys.platform == "darwin":
        return Path(
            "/Library/Application Support/Blackmagic Design/DaVinci Resolve/"
            "Workflow Integration Plugins"
        )
    if sys.platform == "win32":
        program_data = os.environ.get("PROGRAMDATA")
        if not program_data:
            raise RuntimeError("PROGRAMDATA is not set on this Windows system.")
        return (
            Path(program_data)
            / "Blackmagic Design"
            / "DaVinci Resolve"
            / "Support"
            / "Workflow Integration Plugins"
        )
    raise RuntimeError("Unsupported OS: " + sys.platform)
