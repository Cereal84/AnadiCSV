
from pydantic import ValidationError
from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Label, Static, TextArea


class EditorWidget(Static):

    DEFAULT_CSS = """

        EditorWidget > Vertical {
            width: 100%;
        }


        EditorWidget > Vertical > Horizontal {
            margin: 1;
            width: 100%;
        }

        .btn_edit {
            dock: left;
        }

        .btn_save {
            dock: right;
       }

    """

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("File:", id="label_filename"),
            TextArea.code_editor("", id="content_data", language="json", read_only=True,
                                   show_line_numbers=False, theme="monokai"),

            Horizontal(
                Button("Edit", id="btn_edit", variant="warning", classes="btn_edit"),
                Button("Save", id="btn_save", variant="success", disabled=True, classes="btn_save"),
            )
        )
   
    def _render(self):
        # show setting file name
        filename_label = self.query_one("#label_filename", Label)
        filename_label.update(f"File: {self._filename}")

        settings_text = self.query_one("#content_data", TextArea) 
        settings_text.text = Path(self._filename).read_text()

    def _toggle_button(self, btn_id: str):
        btn = self.query_one(f"#{btn_id}", Button)
        btn.disabled = not btn.disabled

    def load_filename(self, filename: str, validation_data = None):
        self._validation_data = validation_data
        self._filename = filename
        self._render()

    def _save_content(self) -> bool:
        content = self.query_one('#content_data', TextArea).text
        if self._validation_data is not None:
            self._validation_data(content)
        with open(self._filename, 'w') as outputfile:
            outputfile.write(content)

    @on(Button.Pressed, "#btn_edit")
    def on_edit_btn_click(self):
        # enable writting
        textarea = self.query_one("#content_data", TextArea)
        textarea.read_only = False
        textarea.show_line_numbers = True

        # enable Save button
        self._toggle_button("btn_save")
    
        # disable Edit button
        self._toggle_button("btn_edit")

    @on(Button.Pressed, "#btn_save")
    def on_save_btn_click(self):

        try:

            self._save_content()

            # disable edit mode
            textarea = self.query_one("#content_data", TextArea)
            textarea.read_only = True
            textarea.show_line_numbers = False

            # enable Save button
            self._toggle_button("btn_save")
    
            # disable Edit button
            self._toggle_button("btn_edit") 

        except ValidationError as ex:
            field_path = ".".join(ex.errors()[0]['loc'])
            err_msg =  ex.errors()[0]['msg']
            msg_error = f"'{field_path}': {err_msg}"
            self.notify(msg_error, severity="error")
        except Exception as ex:
            self.notify(f"{ex}", severity="error")
        else:
            self.notify("Saved")
            return True


 


