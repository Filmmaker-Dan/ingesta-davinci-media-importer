# Ingesta - Media Importer

Version 0.2.1 — cross-platform Workflow Integration script for DaVinci
Resolve Studio 21 (macOS + Windows).

This directory is the source of truth. A mirror also lives at
`~/Projects/resolve-media-importer`.

## Features

- Select individual media files, folders, or a mixed queue
- File/folder pickers: Resolve native dialog → OS fallback (AppleScript /
  PowerShell) → **Use pasted paths** (tkinter is avoided inside Resolve)
- Folder import modes:
  - **Ignore subfolders** — top-level files only, into the selected bin
  - **Replicate folder structure** — mirror nested folders as Media Pool bins
  - **Flatten all media** — import every nested file into the selected bin
- Choose an existing Media Pool bin
- Create nested bins with duplicate-name validation
- Import without changing the active Resolve page
- Apply optional Scene and Description metadata
- Apply an optional Resolve clip colour (Resolve menu order)
- Add and deduplicate comma-separated Keywords
- Optional Website and Donate buttons (open the system browser)
- Refresh bins after project changes
- Print detailed runtime errors to Resolve's Fusion Console

## Requirements

- DaVinci Resolve Studio 21
- macOS or Windows
- No third-party Python packages or separate SDK downloads

## Install (recommended)

Keep this folder as the source of truth. Do not edit the deployed copy inside
Resolve.

### macOS

1. Double-click `install.command`, **or** run:

   ```bash
   python3 install.py
   ```

2. If permission is denied, retry with:

   ```bash
   sudo python3 install.py
   ```

3. Fully quit and reopen Resolve Studio.
4. Open **Workspace → Workflow Integrations → Ingesta - Media Importer**.

Destination:

```text
/Library/Application Support/Blackmagic Design/DaVinci Resolve/Workflow Integration Plugins/
```

### Windows

1. Right-click `install.bat` → **Run as administrator** if needed, **or** run:

   ```bat
   python install.py
   ```

2. Fully quit and reopen Resolve Studio.
3. Open **Workspace → Workflow Integrations → Ingesta - Media Importer**.

Destination:

```text
%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Workflow Integration Plugins\
```

The installer copies only:

- `Ingesta - Media Importer.py`

It also removes legacy `MediaImporter.py` and any stale `media_importer/` package
folder left from earlier multi-file experiments (Resolve loads the single-file
plugin reliably).

## Manual deployment

If you prefer not to use the installer, copy `Ingesta - Media Importer.py` into
the OS destination above, then fully restart Resolve.

## Branding URLs

Edit these constants near the top of `Ingesta - Media Importer.py`:

- `WEBSITE_URL`
- `DONATE_URL`

## Full regression checklist (macOS + Windows)

Run this checklist on both platforms before release:

### Install / launch

- [ ] Fresh Resolve restart → plugin loads
- [ ] Installer places the script in the correct OS folder
- [ ] Plugin appears as **Ingesta - Media Importer**
- [ ] Window opens, closes, and reopens (single-instance)
- [ ] No-project state shows a friendly message

### Bins

- [ ] Existing and nested bins load
- [ ] Refresh preserves the selected bin
- [ ] New and nested bins can be created
- [ ] Blank and duplicate bin names are rejected

### Media queue / pickers

- [ ] File picker (Resolve native) works, or falls back cleanly
- [ ] File picker OS fallback works if Resolve dialog is unavailable
- [ ] **Use pasted paths** validates and queues pasted absolute paths
- [ ] Multiple files can be selected
- [ ] A folder can be selected
- [ ] Files and folders can share one queue
- [ ] Duplicate queued paths are ignored
- [ ] Paths containing spaces and non-ASCII characters work
- [ ] Missing paths are rejected before import

### Import / metadata

- [ ] Media imports into the selected bin
- [ ] **Ignore subfolders** imports only top-level files into the selected bin
- [ ] **Replicate folder structure** creates matching nested bins
- [ ] **Flatten all media** imports nested files into the selected bin without nested bins
- [ ] Resolve stays on the active page
- [ ] Clip colour dropdown uses Resolve's colour order
- [ ] All 16 clip colours work
- [ ] **None** leaves the default clip colour
- [ ] Scene and Description appear in Resolve's Metadata panel
- [ ] Empty Scene/Description fields leave existing clip values untouched
- [ ] Keywords are visible in Resolve's Metadata panel
- [ ] Duplicate Keywords are removed case-insensitively
- [ ] Metadata is applied to every clip in a batch
- [ ] Changing projects refreshes bins before import
- [ ] A second import works without reopening the plugin
- [ ] Import button disables while an import is running

### Branding

- [ ] **Website** opens the configured site in the system browser
- [ ] **Donate** opens the configured donation page in the system browser

## Diagnostics

Normal status messages and full error tracebacks are printed to Resolve's
Fusion Console with an `Ingesta:` prefix. Diagnostics remain in memory for the
current plugin run; the plugin does not create log files.

Picker backends are logged as:

```text
Ingesta: [INFO] File picker backend=fusion|macos|windows
```

## Troubleshooting

- If the menu item is absent, run the installer again and fully restart Resolve.
- If both old and new names appear, delete the old `MediaImporter.py`.
- If a picker fails, paste absolute paths (one per line) and click
  **Use pasted paths**.
- If bins are stale after switching projects, click **Refresh bins**.
- For detailed Python errors, open Resolve's Fusion Console.
- On macOS, `/Library/...` may require `sudo`.
- On Windows, `%PROGRAMDATA%` may require **Run as administrator**.

## Repo layout

```text
resolve-media-importer / PROJECTS/
├── README.md
├── install.py
├── install.command          # macOS
├── install.bat              # Windows
├── Ingesta - Media Importer.py   # deployed plugin (single file)
└── media_importer/
    └── utils/               # shared picker/path helpers (dev reference)
```

The runtime plugin is intentionally a **single file** so Resolve registration
stays reliable. Helper modules under `media_importer/utils/` mirror the picker
design from the implementation plan for maintenance and testing outside Resolve.

## Data and privacy

Ingesta runs locally inside Resolve. It has no analytics, tracking, advertising,
background network requests, cloud storage, or data sharing. Selected paths and
metadata are passed only to the local Resolve project.

**Website** and **Donate** open the system browser only when the user clicks
them. The plugin does not phone home. Any data collected after that is governed
by the destination website (for example a donation host), not by Ingesta.

No App Store / Play Store privacy declarations are required for version 0.2.1.
