"""Main UIManager window for Ingesta - Media Importer."""

from typing import Any, Dict

from media_importer.constants import WINDOW_GEOMETRY, WINDOW_ID, WINDOW_TITLE


def show_main_window(fusion: Any, bmd: Any) -> None:
    """Create the window or focus the existing instance."""
    ui = fusion.UIManager
    dispatcher = bmd.UIDispatcher(ui)

    existing_window = ui.FindWindow(WINDOW_ID)
    if existing_window:
        existing_window.Show()
        existing_window.Raise()
        return

    window = dispatcher.AddWindow(
        {
            "ID": WINDOW_ID,
            "WindowTitle": WINDOW_TITLE,
            "Geometry": WINDOW_GEOMETRY,
        },
        ui.VGroup(
            [
                ui.Label(
                    {
                        "ID": "TitleLabel",
                        "Text": "Ingesta - Media Importer",
                        "Alignment": {"AlignHCenter": True},
                    }
                ),
                ui.Label(
                    {
                        "ID": "StatusLabel",
                        "Text": "Milestone 0 is installed correctly.",
                        "Alignment": {"AlignHCenter": True},
                    }
                ),
                ui.VGap(1),
                ui.Button({"ID": "CloseButton", "Text": "Close", "Weight": 0}),
            ]
        ),
    )

    def close_window(event: Dict[str, Any]) -> None:
        dispatcher.ExitLoop()

    window.On[WINDOW_ID].Close = close_window
    window.On["CloseButton"].Clicked = close_window

    window.Show()
    dispatcher.RunLoop()
