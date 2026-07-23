"""macOS AppleScript file/folder pickers (fallback)."""

from __future__ import annotations

import subprocess


def pick_files() -> list[str]:
    script = """
    set theFiles to choose file with prompt "Select media files" with multiple selections allowed
    set output to ""
    repeat with f in theFiles
        set output to output & POSIX path of f & linefeed
    end repeat
    return output
    """
    result = subprocess.run(
        ["osascript", "-e", script],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        if "User canceled" in stderr or result.returncode == 1:
            return []
        raise RuntimeError(stderr or "macOS file picker failed")

    paths = []
    for line in (result.stdout or "").splitlines():
        line = line.strip()
        if line:
            paths.append(line)
    return paths


def pick_folder() -> str | None:
    script = """
    set theFolder to choose folder with prompt "Select media folder"
    return POSIX path of theFolder
    """
    result = subprocess.run(
        ["osascript", "-e", script],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        if "User canceled" in stderr or result.returncode == 1:
            return None
        raise RuntimeError(stderr or "macOS folder picker failed")

    path = (result.stdout or "").strip()
    return path or None
