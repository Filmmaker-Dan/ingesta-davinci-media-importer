"""Windows PowerShell file/folder pickers (fallback)."""

from __future__ import annotations

import subprocess


def _run_powershell(script: str) -> str:
    result = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            script,
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        raise RuntimeError(stderr or "Windows picker failed")
    return (result.stdout or "").strip()


def pick_files() -> list[str]:
    script = r"""
Add-Type -AssemblyName System.Windows.Forms
$dialog = New-Object System.Windows.Forms.OpenFileDialog
$dialog.Multiselect = $true
$dialog.Title = 'Select media files'
if ($dialog.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) { exit 0 }
$dialog.FileNames -join "`n"
"""
    output = _run_powershell(script)
    if not output:
        return []
    return [line.strip() for line in output.splitlines() if line.strip()]


def pick_folder() -> str | None:
    script = r"""
Add-Type -AssemblyName System.Windows.Forms
$dialog = New-Object System.Windows.Forms.FolderBrowserDialog
$dialog.Description = 'Select media folder'
if ($dialog.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) { exit 0 }
$dialog.SelectedPath
"""
    output = _run_powershell(script)
    return output or None
