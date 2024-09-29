from typing import List

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Label, ListItem, ListView, TextArea


class HistoryCmdModal(Screen[str]):
    """The modal used to asks to quit app."""


    DEFAULT_CSS = """
        HistoryCmdModal {
            align: center middle;
        }

        HistoryCmdModal > Vertical {
            width: 100%;
            height: 100%;
        }

        HistoryCmdModal > Vertical > Label {
             content-align-horizontal: center;
             width: 100%;
        }

        HistoryCmdModal > Vertical > ListView {
            width: 100%;
            height: 80%;
            content-align-horizontal: center;
            margin-top: 1;

            border: solid white;
            border-title-align: center;
        }

        HistoryCmdModal > Vertical > Horizontal {
            width: 99%;
        }

        HistoryCmdModal > Vertical > Horizontal > Button {
            margin: 2;
        }



        HistoryCmdModal > Vertical > ListView > ListItem {
            margin: 2 2;
        }

        TextArea {
            border: none;
        }

        .ignore_history {
            dock: left;
        }


        .select_history {
            dock:right;
        }


    """

    def __init__(self, history: List[str]):
        self._history = history
        self._history.reverse()
        self._selected_item = ""
        super().__init__()


    def compose(self) -> ComposeResult:
        items = []
        for elem in self._history:
            items.append(ListItem(TextArea(elem, language="sql", classes="history_item",
                                           read_only=True)))

        with Vertical():
            yield ListView(*items, id="history_view")
            with Horizontal():
                yield Button("Cancel", id="ignore_history", classes="ignore_history", variant="error")
                yield Button("Select", id="select_history", classes="select_history", variant="success")

    def on_mount(self) -> None:
        history = self.query_one("#history_view", ListView)        
        history.border_title = "HISTORY"



    @on(Button.Pressed, "#select_history")
    def select_item(self) -> None:
        # get SQL selected
        history_view = self.query_one("#history_view", ListView)
        text = history_view.highlighted_child.get_child_by_type(TextArea).text
        self.dismiss(text)

    @on(Button.Pressed, "#ignore_history")
    def back_to_app(self) -> None:
        self.dismiss(None)
