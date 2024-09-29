import os.path

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label


class SaveAsModal(ModalScreen[str]):
    """The modal used to asks a filename to save."""


    DEFAULT_CSS = """
        SaveAsModal {
            align: center middle;
        }

        SaveAsModal > Container {
            width: auto;
            height: auto;
        }

        SaveAsModal > Container > Label {
            width: 100%;
            content-align-horizontal: center;
            margin-top: 1;
        }

        SaveAsModal > Container > Horizontal {
            width: auto;
            height: auto;
        }

        SaveAsModal > Container > Horizontal > Button {
            margin: 2 4;
        }

    """

    def __init__(self, directory: str):
        self._dir = directory
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Container(
            Label("Filename"),
            Input(placeholder="filename", type="text", id="new_filename"),
            Horizontal(
                Button("Cancel", id="btn_cancel", variant="error"),
                Button("Save", id="btn_save_new", variant="success")
            )
        )

    @on(Button.Pressed, "#btn_save_new")
    def save_action(self) -> None:

        # get filename
        filename = str(self.query_one("#new_filename", Input).value)

        # check if already exists
        # add the path
        fullname = os.path.join(self._dir, filename)
        if os.path.exists(fullname):
            self.notify(f"File {fullname} already exists", severity="error")
            return

        self.dismiss(filename)

    @on(Button.Pressed, "#btn_cancel")
    def ignore_action(self) -> None:
        self.app.pop_screen()
