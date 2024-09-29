
from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class QuitAppModal(ModalScreen):
    """The modal used to asks to quit app."""


    DEFAULT_CSS = """
        QuitAppModal {
            align: center middle;
        }

        QuitAppModal > Container {
            width: auto;
            height: auto;
        }

        QuitAppModal > Container > Label {
            width: 100%;
            content-align-horizontal: center;
            margin-top: 1;
        }

        QuitAppModal > Container > Horizontal {
            width: auto;
            height: auto;
        }

        QuitAppModal > Container > Horizontal > Button {
            margin: 2 4;
        }

    """


    def compose(self) -> ComposeResult:
        with Container():
            yield Label("Are you sure you want to quit?")
            with Horizontal():
                yield Button("no", id="no_quit", variant="error")
                yield Button("yes", id="yes_quit", variant="success")


    @on(Button.Pressed, "#yes_quit")
    def exit_app(self) -> None:
        self.app.exit()

    @on(Button.Pressed, "#no_quit")
    def back_to_app(self) -> None:
        self.app.pop_screen()
