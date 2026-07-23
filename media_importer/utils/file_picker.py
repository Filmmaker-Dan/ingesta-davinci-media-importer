"""Public file/folder picker API with tkinter primary and OS fallbacks."""

from __future__ import annotations

import sys

from media_importer.utils import _picker_macos, _picker_tk, _picker_windows
from media_importer.utils.paths import normalize_path


def pick_files() -> list[str]:
    backend = "tk"
    try:
        paths = _picker_tk.pick_files()
    except Exception:
        if sys.platform == "darwin":
            backend = "macos"
            paths = _picker_macos.pick_files()
        elif sys.platform == "win32":
            backend = "windows"
            paths = _picker_windows.pick_files()
        else:
            raise
    print("Ingesta: file picker backend=" + backend)
    return [normalize_path(path) for path in paths if path]


def pick_folder() -> str | None:
    backend = "tk"
    try:
        path = _picker_tk.pick_folder()
    except Exception:
        if sys.platform == "darwin":
            backend = "macos"
            path = _picker_macos.pick_folder()
        elif sys.platform == "win32":
            backend = "windows"
            path = _picker_windows.pick_folder()
        else:
            raise
    print("Ingesta: folder picker backend=" + backend)
    if not path:
        return None
    return normalize_path(path)
