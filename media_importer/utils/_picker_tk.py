"""Tkinter file/folder pickers (primary backend)."""

from __future__ import annotations


def pick_files() -> list[str]:
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    try:
        selected = filedialog.askopenfilenames(parent=root, title="Select media files")
    finally:
        root.destroy()

    if not selected:
        return []
    return [str(path) for path in selected]


def pick_folder() -> str | None:
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    try:
        selected = filedialog.askdirectory(parent=root, title="Select media folder")
    finally:
        root.destroy()

    if not selected:
        return None
    return str(selected)
