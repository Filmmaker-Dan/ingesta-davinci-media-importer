"""Public file/folder picker API with OS-native primary and tkinter last resort.

Inside DaVinci Resolve, prefer fusion.RequestFile / RequestDir instead of this
module. Tkinter often opens a broken fuscript window when hosted by Resolve.
"""

from __future__ import annotations

import sys

from media_importer.utils import _picker_macos, _picker_tk, _picker_windows
from media_importer.utils.paths import normalize_path


def pick_files() -> list[str]:
    errors = []
    backends = []
    if sys.platform == "darwin":
        backends.append(("macos", _picker_macos.pick_files))
    elif sys.platform == "win32":
        backends.append(("windows", _picker_windows.pick_files))
    backends.append(("tk", _picker_tk.pick_files))

    for backend, picker in backends:
        try:
            paths = picker()
            print("Ingesta: file picker backend=" + backend)
            return [normalize_path(path) for path in paths if path]
        except Exception as error:
            errors.append(backend + ": " + str(error))
    raise RuntimeError("All file pickers failed: " + " | ".join(errors))


def pick_folder() -> str | None:
    errors = []
    backends = []
    if sys.platform == "darwin":
        backends.append(("macos", _picker_macos.pick_folder))
    elif sys.platform == "win32":
        backends.append(("windows", _picker_windows.pick_folder))
    backends.append(("tk", _picker_tk.pick_folder))

    for backend, picker in backends:
        try:
            path = picker()
            print("Ingesta: folder picker backend=" + backend)
            if not path:
                return None
            return normalize_path(path)
        except Exception as error:
            errors.append(backend + ": " + str(error))
    raise RuntimeError("All folder pickers failed: " + " | ".join(errors))
