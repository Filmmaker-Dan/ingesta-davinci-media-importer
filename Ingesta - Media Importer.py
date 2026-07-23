"""Ingesta - Media Importer for DaVinci Resolve."""

import ast
import os
import subprocess
import sys
import traceback
import webbrowser
from pathlib import Path

PLUGIN_VERSION = "0.2.0"
WINDOW_ID = "com.dangoetz.resolve.ingesta_media_importer"
BIN_TREE_ID = "BinTree"
STATUS_LABEL_ID = "StatusLabel"
SELECTED_BIN_LABEL_ID = "SelectedBinLabel"
NEW_BIN_NAME_ID = "NewBinName"
CREATE_BIN_BUTTON_ID = "CreateBinButton"
PATH_QUEUE_ID = "PathQueue"
IMPORT_BUTTON_ID = "ImportButton"
FOLDER_IMPORT_MODE_ID = "FolderImportMode"
CLIP_COLOR_ID = "ClipColor"
KEYWORDS_ID = "Keywords"
SCENE_ID = "Scene"
DESCRIPTION_ID = "Description"
WEBSITE_BUTTON_ID = "WebsiteButton"
DONATE_BUTTON_ID = "DonateButton"
USE_PASTED_PATHS_BUTTON_ID = "UsePastedPathsButton"

# Replace these with your live pages before shipping.
WEBSITE_URL = "https://www.goetz.video"
DONATE_URL = "https://buymeacoffee.com/instagotz"

FOLDER_IMPORT_MODE_IGNORE = "Ignore subfolders"
FOLDER_IMPORT_MODE_REPLICATE = "Replicate folder structure"
FOLDER_IMPORT_MODE_FLATTEN = "Flatten all media"
FOLDER_IMPORT_MODES = [
    FOLDER_IMPORT_MODE_IGNORE,
    FOLDER_IMPORT_MODE_REPLICATE,
    FOLDER_IMPORT_MODE_FLATTEN,
]

# Ordered to match DaVinci Resolve's clip colour menu.
CLIP_COLORS = [
    "None",
    "Orange",
    "Apricot",
    "Yellow",
    "Lime",
    "Olive",
    "Green",
    "Teal",
    "Navy",
    "Blue",
    "Purple",
    "Violet",
    "Pink",
    "Tan",
    "Beige",
    "Brown",
    "Chocolate",
]

ui = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)

window = ui.FindWindow(WINDOW_ID)
if window:
    window.Show()
    window.Raise()
else:
    window = dispatcher.AddWindow(
        {
            "ID": WINDOW_ID,
            "WindowTitle": "Ingesta - Media Importer",
            "Geometry": [200, 80, 720, 860],
        },
        ui.VGroup(
            [
                ui.Label(
                    {
                        "Text": "Ingesta - Media Importer",
                        "Font": ui.Font({"PointSize": 16, "Bold": True}),
                        "Alignment": {"AlignHCenter": True},
                        "Weight": 0,
                    }
                ),
                ui.Label(
                    {
                        "Text": "Version " + PLUGIN_VERSION + "  ·  Free tool",
                        "Alignment": {"AlignHCenter": True},
                        "Weight": 0,
                    }
                ),
                ui.Label(
                    {
                        "Text": "Media to import",
                        "Weight": 0,
                    }
                ),
                ui.HGroup(
                    {"Weight": 0},
                    [
                        ui.Button({"ID": "AddFilesButton", "Text": "Add files"}),
                        ui.Button({"ID": "AddFolderButton", "Text": "Add folder"}),
                        ui.Button({"ID": "ClearPathsButton", "Text": "Clear"}),
                        ui.Button(
                            {
                                "ID": USE_PASTED_PATHS_BUTTON_ID,
                                "Text": "Use pasted paths",
                            }
                        ),
                        ui.HGap(1),
                    ],
                ),
                ui.HGroup(
                    {"Weight": 0},
                    [
                        ui.Label(
                            {
                                "Text": "Folder import",
                                "Weight": 0,
                            }
                        ),
                        ui.ComboBox(
                            {
                                "ID": FOLDER_IMPORT_MODE_ID,
                                "Weight": 1,
                            }
                        ),
                    ],
                ),
                ui.TextEdit(
                    {
                        "ID": PATH_QUEUE_ID,
                        "PlaceholderText": "No media selected. Use Add files / Add folder, or paste absolute paths (one per line) then click Use pasted paths.",
                        "Weight": 0.3,
                    }
                ),
                ui.Label(
                    {
                        "Text": "Select a destination bin",
                        "Weight": 0,
                    }
                ),
                ui.Tree(
                    {
                        "ID": BIN_TREE_ID,
                        "ColumnCount": 1,
                        "HeaderHidden": True,
                        "RootIsDecorated": True,
                        "ItemsExpandable": True,
                        "ExpandsOnDoubleClick": True,
                        "AlternatingRowColors": True,
                        "SelectionMode": "SingleSelection",
                        "Weight": 0.4,
                    }
                ),
                ui.Label(
                    {
                        "ID": SELECTED_BIN_LABEL_ID,
                        "Text": "Selected bin: None",
                        "Weight": 0,
                    }
                ),
                ui.Label(
                    {
                        "Text": "Create a new bin inside the selected bin",
                        "Weight": 0,
                    }
                ),
                ui.HGroup(
                    {"Weight": 0},
                    [
                        ui.LineEdit(
                            {
                                "ID": NEW_BIN_NAME_ID,
                                "PlaceholderText": "New bin name",
                                "Weight": 1,
                            }
                        ),
                        ui.Button(
                            {
                                "ID": CREATE_BIN_BUTTON_ID,
                                "Text": "Create bin",
                                "Weight": 0,
                            }
                        ),
                    ],
                ),
                ui.Label(
                    {
                        "Text": "Clip metadata",
                        "Weight": 0,
                    }
                ),
                ui.HGroup(
                    {"Weight": 0},
                    [
                        ui.Label(
                            {
                                "Text": "Scene",
                                "Weight": 0,
                            }
                        ),
                        ui.LineEdit(
                            {
                                "ID": SCENE_ID,
                                "PlaceholderText": "e.g. 12A",
                                "Weight": 0.35,
                            }
                        ),
                        ui.Label(
                            {
                                "Text": "Description",
                                "Weight": 0,
                            }
                        ),
                        ui.LineEdit(
                            {
                                "ID": DESCRIPTION_ID,
                                "PlaceholderText": "What this clip is",
                                "Weight": 0.65,
                            }
                        ),
                    ],
                ),
                ui.HGroup(
                    {"Weight": 0},
                    [
                        ui.Label(
                            {
                                "Text": "Clip colour",
                                "Weight": 0,
                            }
                        ),
                        ui.ComboBox(
                            {
                                "ID": CLIP_COLOR_ID,
                                "Weight": 0.35,
                            }
                        ),
                        ui.Label(
                            {
                                "Text": "Keywords",
                                "Weight": 0,
                            }
                        ),
                        ui.LineEdit(
                            {
                                "ID": KEYWORDS_ID,
                                "PlaceholderText": "interview, b-roll, hero",
                                "Weight": 0.65,
                            }
                        ),
                    ],
                ),
                ui.Label(
                    {
                        "ID": STATUS_LABEL_ID,
                        "Text": "Loading bins...",
                        "WordWrap": True,
                        "Weight": 0,
                    }
                ),
                ui.Button(
                    {
                        "ID": IMPORT_BUTTON_ID,
                        "Text": "Import media into selected bin",
                        "Weight": 0,
                    }
                ),
                ui.HGroup(
                    {"Weight": 0},
                    [
                        ui.Button(
                            {
                                "ID": "RefreshButton",
                                "Text": "Refresh bins",
                                "Weight": 1,
                            }
                        ),
                        ui.Button(
                            {
                                "ID": "CloseButton",
                                "Text": "Close",
                                "Weight": 1,
                            }
                        ),
                    ],
                ),
                ui.HGroup(
                    {"Weight": 0},
                    [
                        ui.HGap(0, 1.0),
                        ui.Button(
                            {
                                "ID": WEBSITE_BUTTON_ID,
                                "Text": "Website",
                                "Weight": 0,
                            }
                        ),
                        ui.Button(
                            {
                                "ID": DONATE_BUTTON_ID,
                                "Text": "Donate",
                                "Weight": 0,
                            }
                        ),
                        ui.HGap(0, 1.0),
                    ],
                ),
            ]
        ),
    )

    items = window.GetItems()
    bin_tree = items[BIN_TREE_ID]
    folder_by_id = {}
    item_by_folder_id = {}
    selected_folder = {"value": None}
    selected_project_id = {"value": None}
    diagnostic_log = []
    items[CLIP_COLOR_ID].AddItems(CLIP_COLORS)
    items[CLIP_COLOR_ID].CurrentIndex = 0
    items[FOLDER_IMPORT_MODE_ID].AddItems(FOLDER_IMPORT_MODES)
    items[FOLDER_IMPORT_MODE_ID].CurrentIndex = FOLDER_IMPORT_MODES.index(
        FOLDER_IMPORT_MODE_REPLICATE
    )

    def log_message(level, message):
        entry = "[" + level + "] " + str(message)
        diagnostic_log.append(entry)
        print("Ingesta: " + entry)

    def set_status(message):
        items[STATUS_LABEL_ID].Text = message
        log_message("INFO", message)

    def report_error(context, error):
        details = traceback.format_exc()
        log_message("ERROR", context + ": " + str(error))
        print(details)
        items[STATUS_LABEL_ID].Text = context + ": " + str(error)

    def normalize_path(path):
        raw = str(path).strip().strip('"')
        if not raw:
            return ""
        try:
            return str(Path(raw).expanduser().resolve())
        except OSError:
            return os.path.normpath(os.path.expanduser(raw))

    def pick_files_tk():
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        try:
            root.attributes("-topmost", True)
        except Exception:
            pass
        try:
            selected = filedialog.askopenfilenames(
                parent=root, title="Select media files"
            )
        finally:
            root.destroy()
        if not selected:
            return []
        return [str(path) for path in selected]

    def pick_folder_tk():
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        try:
            root.attributes("-topmost", True)
        except Exception:
            pass
        try:
            selected = filedialog.askdirectory(
                parent=root, title="Select media folder"
            )
        finally:
            root.destroy()
        if not selected:
            return None
        return str(selected)

    def pick_files_macos():
        script = (
            'set theFiles to choose file with prompt "Select media files" '
            "with multiple selections allowed\n"
            'set output to ""\n'
            "repeat with f in theFiles\n"
            "set output to output & POSIX path of f & linefeed\n"
            "end repeat\n"
            "return output"
        )
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
        return [
            line.strip()
            for line in (result.stdout or "").splitlines()
            if line.strip()
        ]

    def pick_folder_macos():
        script = (
            'set theFolder to choose folder with prompt "Select media folder"\n'
            "return POSIX path of theFolder"
        )
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

    def pick_files_windows():
        script = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            "$d = New-Object System.Windows.Forms.OpenFileDialog; "
            "$d.Multiselect = $true; $d.Title = 'Select media files'; "
            "if ($d.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) { exit 0 }; "
            "$d.FileNames -join \"`n\""
        )
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
            raise RuntimeError((result.stderr or "").strip() or "Windows file picker failed")
        output = (result.stdout or "").strip()
        if not output:
            return []
        return [line.strip() for line in output.splitlines() if line.strip()]

    def pick_folder_windows():
        script = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            "$d = New-Object System.Windows.Forms.FolderBrowserDialog; "
            "$d.Description = 'Select media folder'; "
            "if ($d.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) { exit 0 }; "
            "$d.SelectedPath"
        )
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
            raise RuntimeError(
                (result.stderr or "").strip() or "Windows folder picker failed"
            )
        output = (result.stdout or "").strip()
        return output or None

    def pick_files_fusion():
        if not hasattr(fusion, "RequestFile"):
            raise RuntimeError("fusion.RequestFile is unavailable")
        selected = fusion.RequestFile("", "", {"FReqB_Multi": True})
        return paths_from_file_request(selected)

    def pick_folder_fusion():
        if not hasattr(fusion, "RequestDir"):
            raise RuntimeError("fusion.RequestDir is unavailable")
        selected = fusion.RequestDir()
        if not selected:
            return None
        return normalize_path(selected)

    def pick_files():
        errors = []
        for backend, picker in (
            ("tk", pick_files_tk),
            (
                "macos" if sys.platform == "darwin" else "windows",
                pick_files_macos if sys.platform == "darwin" else pick_files_windows,
            ),
            ("fusion", pick_files_fusion),
        ):
            if backend == "windows" and sys.platform != "win32":
                continue
            if backend == "macos" and sys.platform != "darwin":
                continue
            try:
                paths = picker()
                log_message("INFO", "File picker backend=" + backend)
                return [normalize_path(path) for path in paths if path]
            except Exception as error:
                errors.append(backend + ": " + str(error))
        raise RuntimeError(
            "All file pickers failed. Paste absolute paths and click "
            "Use pasted paths. Details: "
            + " | ".join(errors)
        )

    def pick_folder():
        errors = []
        for backend, picker in (
            ("tk", pick_folder_tk),
            (
                "macos" if sys.platform == "darwin" else "windows",
                pick_folder_macos if sys.platform == "darwin" else pick_folder_windows,
            ),
            ("fusion", pick_folder_fusion),
        ):
            if backend == "windows" and sys.platform != "win32":
                continue
            if backend == "macos" and sys.platform != "darwin":
                continue
            try:
                path = picker()
                log_message("INFO", "Folder picker backend=" + backend)
                if not path:
                    return None
                return normalize_path(path)
            except Exception as error:
                errors.append(backend + ": " + str(error))
        raise RuntimeError(
            "All folder pickers failed. Paste an absolute folder path and click "
            "Use pasted paths. Details: "
            + " | ".join(errors)
        )

    def get_queued_paths():
        text = items[PATH_QUEUE_ID].PlainText or ""
        paths = []
        for line in text.splitlines():
            line = line.strip().strip('"')
            if not line:
                continue
            path = normalize_path(line)
            if path not in paths:
                paths.append(path)
        return paths

    def set_queued_paths(paths):
        unique_paths = []
        for path in paths:
            normalized = normalize_path(path)
            if normalized and normalized not in unique_paths:
                unique_paths.append(normalized)
        items[PATH_QUEUE_ID].PlainText = "\n".join(unique_paths)
        return unique_paths

    def paths_from_file_request(selected):
        if not selected:
            return []

        if isinstance(selected, str):
            return [normalize_path(selected)]

        try:
            path_dict = dict(selected)
        except Exception:
            path_dict = ast.literal_eval(str(selected))

        if not isinstance(path_dict, dict):
            return []

        parent = path_dict.pop("Path", "")
        paths = []
        for child in path_dict.values():
            paths.append(normalize_path(os.path.join(parent, str(child))))
        return paths

    def add_paths(new_paths):
        if not new_paths:
            set_status("No media was selected.")
            return

        combined = get_queued_paths()
        added = 0
        for path in new_paths:
            normalized = normalize_path(path)
            if normalized and normalized not in combined:
                combined.append(normalized)
                added += 1

        set_queued_paths(combined)
        skipped = len(new_paths) - added
        if skipped > 0:
            set_status(
                "Added "
                + str(added)
                + " path(s). Skipped "
                + str(skipped)
                + " duplicate(s). Queue now has "
                + str(len(combined))
                + " path(s)."
            )
        else:
            set_status(
                "Added "
                + str(added)
                + " path(s). Queue now has "
                + str(len(combined))
                + " path(s)."
            )

    def add_files(event):
        try:
            add_paths(pick_files())
        except Exception as error:
            report_error("Could not open the file picker", error)

    def add_folder(event):
        try:
            selected = pick_folder()
            if not selected:
                set_status("No folder was selected.")
                return
            add_paths([selected])
        except Exception as error:
            report_error("Could not open the folder picker", error)

    def use_pasted_paths(event):
        paths = get_queued_paths()
        if not paths:
            set_status(
                "Paste absolute file or folder paths into the list (one per line), "
                "then click Use pasted paths."
            )
            return
        missing = [path for path in paths if not os.path.exists(path)]
        if missing:
            set_status(
                "Pasted path does not exist: "
                + missing[0]
                + ". Fix the path(s) and try again."
            )
            return
        set_queued_paths(paths)
        set_status(
            "Using "
            + str(len(paths))
            + " pasted path(s). Ready to import."
        )

    def clear_paths(event):
        items[PATH_QUEUE_ID].PlainText = ""
        set_status("Media queue cleared.")

    def add_folder_to_tree(folder, parent_item=None):
        folder_id = str(folder.GetUniqueId())
        folder_by_id[folder_id] = folder

        tree_item = bin_tree.NewItem()
        tree_item.Text[0] = folder.GetName()
        tree_item.ToolTip[0] = folder_id
        item_by_folder_id[folder_id] = tree_item

        if parent_item:
            parent_item.AddChild(tree_item)
        else:
            bin_tree.AddTopLevelItem(tree_item)

        subfolders = list(folder.GetSubFolderList() or [])
        subfolders.sort(key=lambda child: child.GetName().lower())
        for subfolder in subfolders:
            add_folder_to_tree(subfolder, tree_item)

        return tree_item

    def load_bins(preferred_folder_id=None):
        bin_tree.Clear()
        folder_by_id.clear()
        item_by_folder_id.clear()
        selected_folder["value"] = None
        selected_project_id["value"] = None
        items[SELECTED_BIN_LABEL_ID].Text = "Selected bin: None"

        project_manager = resolve.GetProjectManager()
        current_project = project_manager.GetCurrentProject()
        if not current_project:
            set_status("No project is open. Open a project, then click Refresh bins.")
            return
        selected_project_id["value"] = str(current_project.GetUniqueId())

        media_pool = current_project.GetMediaPool()
        root_folder = media_pool.GetRootFolder()
        if not root_folder:
            set_status("Resolve did not return the Media Pool root bin.")
            return

        root_item = add_folder_to_tree(root_folder)
        root_item.Expanded = True

        selected_id = preferred_folder_id
        if selected_id not in folder_by_id:
            selected_id = str(root_folder.GetUniqueId())

        selected_item = item_by_folder_id[selected_id]
        selected_item.Selected = True
        bin_tree.ScrollToItem(selected_item)
        selected_folder["value"] = folder_by_id[selected_id]
        items[SELECTED_BIN_LABEL_ID].Text = (
            "Selected bin: " + selected_folder["value"].GetName()
        )
        set_status("Bins loaded from project: " + current_project.GetName())

    def select_current_bin(event):
        current_item = bin_tree.CurrentItem()
        if not current_item:
            return

        folder_id = str(current_item.ToolTip[0])
        folder = folder_by_id.get(folder_id)
        if not folder:
            set_status("The selected bin could not be resolved. Refresh the bins.")
            return

        selected_folder["value"] = folder
        items[SELECTED_BIN_LABEL_ID].Text = "Selected bin: " + folder.GetName()
        queue_count = len(get_queued_paths())
        set_status(
            "Selected bin ready. Media queue has " + str(queue_count) + " path(s)."
        )

    def refresh_bins(event):
        try:
            selected_id = None
            if selected_folder["value"]:
                selected_id = str(selected_folder["value"].GetUniqueId())
            load_bins(selected_id)
        except Exception as error:
            report_error("Could not load bins", error)

    def create_bin(event):
        try:
            parent_folder = selected_folder["value"]
            if not parent_folder:
                set_status("Select a parent bin before creating a new bin.")
                return

            bin_name = items[NEW_BIN_NAME_ID].Text.strip()
            if not bin_name:
                set_status("Enter a name for the new bin.")
                items[NEW_BIN_NAME_ID].SetFocus("OtherFocusReason")
                return

            sibling_names = [
                child.GetName().lower()
                for child in list(parent_folder.GetSubFolderList() or [])
            ]
            if bin_name.lower() in sibling_names:
                set_status(
                    'A bin named "' + bin_name + '" already exists in this bin.'
                )
                items[NEW_BIN_NAME_ID].SelectAll()
                items[NEW_BIN_NAME_ID].SetFocus("OtherFocusReason")
                return

            current_project = resolve.GetProjectManager().GetCurrentProject()
            if not current_project:
                set_status("No project is open.")
                return

            media_pool = current_project.GetMediaPool()
            new_folder = media_pool.AddSubFolder(parent_folder, bin_name)
            if not new_folder:
                set_status("Resolve could not create the new bin.")
                return

            new_folder_id = str(new_folder.GetUniqueId())
            items[NEW_BIN_NAME_ID].Text = ""
            load_bins(new_folder_id)
            set_status('Created bin "' + bin_name + '" and selected it.')
        except Exception as error:
            report_error("Could not create bin", error)

    def parse_keywords(value):
        keywords = []
        seen = set()
        for keyword in str(value or "").split(","):
            cleaned = keyword.strip()
            normalized = cleaned.lower()
            if cleaned and normalized not in seen:
                keywords.append(cleaned)
                seen.add(normalized)
        return keywords

    def merge_keywords(existing_value, new_keywords):
        merged = parse_keywords(existing_value)
        seen = {keyword.lower() for keyword in merged}
        for keyword in new_keywords:
            normalized = keyword.lower()
            if normalized not in seen:
                merged.append(keyword)
                seen.add(normalized)
        return ", ".join(merged)

    def set_item_keywords(media_pool_item, new_keywords):
        metadata = media_pool_item.GetMetadata() or {}
        discovered_keys = [
            str(key)
            for key in metadata.keys()
            if str(key).lower() in ("keyword", "keywords")
        ]

        candidate_keys = discovered_keys + ["Keywords", "Keyword"]
        tried_keys = set()
        for key in candidate_keys:
            if key in tried_keys:
                continue
            tried_keys.add(key)

            existing_value = media_pool_item.GetMetadata(key) or ""
            merged_value = merge_keywords(existing_value, new_keywords)
            if media_pool_item.SetMetadata(key, merged_value):
                return True

        return False

    def apply_metadata(media_pool_item, clip_color, keywords, scene, description):
        succeeded = True
        if clip_color != "None":
            succeeded = bool(media_pool_item.SetClipColor(clip_color)) and succeeded
        if scene:
            succeeded = bool(media_pool_item.SetMetadata("Scene", scene)) and succeeded
        if description:
            succeeded = (
                bool(media_pool_item.SetMetadata("Description", description))
                and succeeded
            )
        if keywords:
            succeeded = set_item_keywords(media_pool_item, keywords) and succeeded
        return succeeded

    def find_child_folder_by_name(parent_folder, name):
        for child in list(parent_folder.GetSubFolderList() or []):
            if child.GetName() == name:
                return child
        return None

    def ensure_subfolder(media_pool, parent_folder, name):
        existing = find_child_folder_by_name(parent_folder, name)
        if existing:
            return existing
        return media_pool.AddSubFolder(parent_folder, name)

    def list_media_files(directory):
        try:
            entries = sorted(os.listdir(directory), key=lambda name: name.lower())
        except OSError as error:
            raise OSError(
                'Could not read folder "' + directory + '": ' + str(error)
            )

        files = []
        for entry in entries:
            if entry.startswith("."):
                continue
            full_path = os.path.join(directory, entry)
            if os.path.isfile(full_path):
                files.append(full_path)
        return files

    def list_media_files_recursive(directory):
        files = []
        for root, dirnames, filenames in os.walk(directory):
            dirnames[:] = sorted(
                [name for name in dirnames if not name.startswith(".")],
                key=lambda name: name.lower(),
            )
            for filename in sorted(filenames, key=lambda name: name.lower()):
                if filename.startswith("."):
                    continue
                full_path = os.path.join(root, filename)
                if os.path.isfile(full_path):
                    files.append(full_path)
        return files

    def list_subdirectories(directory):
        try:
            entries = sorted(os.listdir(directory), key=lambda name: name.lower())
        except OSError as error:
            raise OSError(
                'Could not read folder "' + directory + '": ' + str(error)
            )

        folders = []
        for entry in entries:
            if entry.startswith("."):
                continue
            full_path = os.path.join(directory, entry)
            if os.path.isdir(full_path):
                folders.append(full_path)
        return folders

    def import_files_into_bin(media_pool, pool_folder, file_paths):
        if not file_paths:
            return []
        if not media_pool.SetCurrentFolder(pool_folder):
            raise RuntimeError(
                'Resolve could not select bin "' + pool_folder.GetName() + '".'
            )
        return list(media_pool.ImportMedia(file_paths) or [])

    def import_folder_tree(media_pool, disk_folder, pool_parent):
        folder_name = os.path.basename(disk_folder.rstrip("\\/"))
        if not folder_name:
            raise RuntimeError(
                'Could not determine a bin name for "' + disk_folder + '".'
            )

        pool_folder = ensure_subfolder(media_pool, pool_parent, folder_name)
        if not pool_folder:
            raise RuntimeError(
                'Resolve could not create or find bin "' + folder_name + '".'
            )

        imported_items = import_files_into_bin(
            media_pool, pool_folder, list_media_files(disk_folder)
        )
        for subfolder in list_subdirectories(disk_folder):
            imported_items.extend(
                import_folder_tree(media_pool, subfolder, pool_folder)
            )
        return imported_items

    def import_queued_paths(media_pool, target_folder, queued_paths, folder_mode):
        imported_items = []
        for path in queued_paths:
            if os.path.isfile(path):
                imported_items.extend(
                    import_files_into_bin(media_pool, target_folder, [path])
                )
                continue

            if not os.path.isdir(path):
                raise RuntimeError(
                    'Path is neither a file nor a folder: "' + path + '".'
                )

            if folder_mode == FOLDER_IMPORT_MODE_REPLICATE:
                imported_items.extend(
                    import_folder_tree(media_pool, path, target_folder)
                )
            elif folder_mode == FOLDER_IMPORT_MODE_FLATTEN:
                imported_items.extend(
                    import_files_into_bin(
                        media_pool, target_folder, list_media_files_recursive(path)
                    )
                )
            else:
                imported_items.extend(
                    import_files_into_bin(
                        media_pool, target_folder, list_media_files(path)
                    )
                )
        return imported_items

    def import_media(event):
        import_button = items[IMPORT_BUTTON_ID]
        import_button.Enabled = False
        import_button.Text = "Importing..."

        try:
            current_project = resolve.GetProjectManager().GetCurrentProject()
            if not current_project:
                set_status("No project is open.")
                return
            current_project_id = str(current_project.GetUniqueId())
            if current_project_id != selected_project_id["value"]:
                load_bins()
                set_status(
                    "The open project changed. Bins were refreshed; confirm the destination bin."
                )
                return

            target_folder = selected_folder["value"]
            if not target_folder:
                set_status("Select a destination bin before importing.")
                return

            queued_paths = get_queued_paths()
            if not queued_paths:
                set_status("Add at least one file or folder before importing.")
                return

            missing_paths = [
                path for path in queued_paths if not os.path.exists(path)
            ]
            if missing_paths:
                set_status(
                    "Cannot import because this path does not exist: "
                    + missing_paths[0]
                )
                return

            media_pool = current_project.GetMediaPool()
            folder_mode = items[FOLDER_IMPORT_MODE_ID].CurrentText
            if folder_mode not in FOLDER_IMPORT_MODES:
                folder_mode = FOLDER_IMPORT_MODE_REPLICATE
            target_folder_id = str(target_folder.GetUniqueId())

            log_message(
                "INFO",
                "Starting import of "
                + str(len(queued_paths))
                + ' queued path(s) into "'
                + target_folder.GetName()
                + '". Folder import mode='
                + folder_mode
                + ".",
            )
            imported_items = import_queued_paths(
                media_pool, target_folder, queued_paths, folder_mode
            )
            if not imported_items:
                set_status(
                    "Resolve did not import any clips. Check the media formats and paths."
                )
                return

            clip_color = items[CLIP_COLOR_ID].CurrentText
            keywords = parse_keywords(items[KEYWORDS_ID].Text)
            scene = items[SCENE_ID].Text.strip()
            description = items[DESCRIPTION_ID].Text.strip()
            metadata_requested = (
                clip_color != "None"
                or bool(keywords)
                or bool(scene)
                or bool(description)
            )
            metadata_failures = []

            if metadata_requested:
                for media_pool_item in imported_items:
                    if not apply_metadata(
                        media_pool_item,
                        clip_color,
                        keywords,
                        scene,
                        description,
                    ):
                        metadata_failures.append(media_pool_item.GetName())

            target_name = target_folder.GetName()
            items[PATH_QUEUE_ID].PlainText = ""
            load_bins(target_folder_id)
            message = (
                "Imported "
                + str(len(imported_items))
                + ' clip(s) into "'
                + target_name
                + '".'
            )
            if folder_mode == FOLDER_IMPORT_MODE_REPLICATE:
                message += " Folder structure was mirrored as bins."
            elif folder_mode == FOLDER_IMPORT_MODE_FLATTEN:
                message += " Nested media was flattened into the selected bin."
            else:
                message += " Subfolders were ignored."
            if metadata_failures:
                message += (
                    " Metadata could not be fully applied to "
                    + str(len(metadata_failures))
                    + " clip(s)."
                )
            elif metadata_requested:
                message += " Selected metadata was applied."
            set_status(message)
        except Exception as error:
            report_error("Import failed", error)
        finally:
            import_button.Enabled = True
            import_button.Text = "Import media into selected bin"

    def close_window(event):
        dispatcher.ExitLoop()

    def open_external_url(url, label):
        if not url or "example.com" in url or url.endswith("/example"):
            set_status(
                "Set "
                + label
                + " URL in the plugin script before shipping (WEBSITE_URL / DONATE_URL)."
            )
            return
        try:
            if not webbrowser.open(url):
                set_status("Could not open the browser for " + label + ".")
                return
            set_status("Opened " + label + " in your browser.")
        except Exception as error:
            report_error("Could not open " + label, error)

    def open_website(event):
        open_external_url(WEBSITE_URL, "Website")

    def open_donate(event):
        open_external_url(DONATE_URL, "Donate")

    window.On[WINDOW_ID].Close = close_window
    window.On.CloseButton.Clicked = close_window
    window.On.RefreshButton.Clicked = refresh_bins
    window.On[WEBSITE_BUTTON_ID].Clicked = open_website
    window.On[DONATE_BUTTON_ID].Clicked = open_donate
    window.On[BIN_TREE_ID].CurrentItemChanged = select_current_bin
    window.On[CREATE_BIN_BUTTON_ID].Clicked = create_bin
    window.On[NEW_BIN_NAME_ID].ReturnPressed = create_bin
    window.On.AddFilesButton.Clicked = add_files
    window.On.AddFolderButton.Clicked = add_folder
    window.On.ClearPathsButton.Clicked = clear_paths
    window.On[USE_PASTED_PATHS_BUTTON_ID].Clicked = use_pasted_paths
    window.On[IMPORT_BUTTON_ID].Clicked = import_media

    refresh_bins(None)
    window.Show()
    dispatcher.RunLoop()
