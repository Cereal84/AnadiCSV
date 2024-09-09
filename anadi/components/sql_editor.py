

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Label, Static, TextArea


class SQLEditor(Static):

   DEFAULT_CSS = """

       SQLEditor > Vertical {
           height: auto;
       }

       SQLEditor > Vertical > TextArea {
           height: 1fr;
           border: solid white;
       }

   """
   def compose(self) -> ComposeResult:

       yield Vertical(
           TextArea.code_editor("", language="sql", show_line_numbers=False,
                                id="sql", classes="sql_editor", theme="monokai", read_only=True),
           Horizontal(
                Button("Run", id="btn_run", classes="btn_run", variant="success", disabled=True)
           )

       )

   def on_mount(self) -> None:
        editor = self.query_one("#sql", TextArea)
        editor.border_title = "SQL Editor"

   def render_sql_query(self, query: str):
        editor = self.query_one("#sql", TextArea)
        editor.text = query

   def enable(self):
        run_btn = self.query_one("#btn_run", Button)
        run_btn.disabled = False

        sql_code = self.query_one("#sql", TextArea)
        sql_code.read_only = False



