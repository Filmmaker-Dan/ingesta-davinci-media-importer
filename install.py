#!/usr/bin/env python3
"""Install Ingesta - Media Importer into DaVinci Resolve Workflow Integration Plugins."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


PLUGIN_FILENAME = "Ingesta - Media Importer.py"
LEGACY_FILENAMES = ("MediaImporter.py",)


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


def source_plugin() -> Path:
    return Path(__file__).resolve().parent / PLUGIN_FILENAME


def install() -> int:
    source = source_plugin()
    if not source.is_file():
        print("ERROR: Missing plugin file:")
        print("  " + str(source))
        return 1

    destination_root = plugins_dir()
    destination = destination_root / PLUGIN_FILENAME

    print("Ingesta installer")
    print("  Source:      " + str(source))
    print("  Destination: " + str(destination))

    try:
        destination_root.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    except PermissionError:
        print("")
        print("ERROR: Permission denied while copying into the plugins folder.")
        if sys.platform == "darwin":
            print("Retry with administrator rights, for example:")
            print('  sudo python3 "' + str(Path(__file__).resolve()) + '"')
        else:
            print('Re-run install.bat using "Run as administrator".')
        return 1
    except OSError as error:
        print("ERROR: Could not install the plugin: " + str(error))
        return 1

    removed_legacy = []
    for legacy_name in LEGACY_FILENAMES:
        legacy_path = destination_root / legacy_name
        if legacy_path.is_file():
            try:
                legacy_path.unlink()
                removed_legacy.append(legacy_name)
            except OSError as error:
                print(
                    "WARNING: Could not remove legacy file "
                    + legacy_name
                    + ": "
                    + str(error)
                )

    # Remove stale multi-file package copies from earlier experiments.
    stale_package = destination_root / "media_importer"
    if stale_package.is_dir():
        try:
            shutil.rmtree(stale_package)
            print("Removed stale package folder: media_importer/")
        except OSError as error:
            print("WARNING: Could not remove stale media_importer/: " + str(error))

    print("")
    print("Installed successfully:")
    print("  " + str(destination))
    if removed_legacy:
        print("Removed legacy menu entries: " + ", ".join(removed_legacy))
    print("")
    print("Next steps:")
    print("  1. Fully quit DaVinci Resolve Studio")
    print("  2. Reopen Resolve")
    print("  3. Open Workspace → Workflow Integrations → Ingesta - Media Importer")
    return 0


if __name__ == "__main__":
    sys.exit(install())
