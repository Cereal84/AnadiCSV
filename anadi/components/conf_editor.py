import os

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.validation import Number, ValidationResult, Validator
from textual.widgets import (Button, Input, Label, Rule, Select, Static,
                             Switch, TextArea)

from anadi.constants import ANADI_CUSTOM_CONFS, ANADI_DEFAULT_CONF_FILE
from anadi.modals.save_as import SaveAsModal
from anadi.models.confs import SettingsDB


class EventCSVConfAssociationChanged(Message):
    """This message is used as Event in order to say to the APP
    to update the csvdb istance and the sidebar infos
    """

    def __init__(self, confname: str) -> None:
        self.confname = confname
        super().__init__()


class ConfEditorWidget(Static):

    DEFAULT_CSS = """

        ConfEditorWidget > Vertical {
            width: 100%;
        }


        ConfEditorWidget > Vertical > Horizontal {
            margin: 1;
            width: 100%;
        }


        .btn_edit {
            dock: right;
        }

        .btn_save {
            dock: left;
            margin: 0 1;
       }

       .label_switch {
           height: 3;
           content-align: center middle;
           width: auto;
       }

       .switch_container {
           height: auto;
       }

       .configuration_data {
           border: solid white;
           padding: 1 1 1 1;
       }

    """

    def compose(self) -> ComposeResult:
        yield Vertical(
            Horizontal(
                Label("Configuration", classes="label_switch"),
                Select(id="conf_list", options=[]),
                Button("Apply", id="change_conf_file_btn"),
                classes="switch_container",
            ),
            Vertical(
                Horizontal(
                    Label("CSV Delimitator", classes="label_switch"),
                    Input(id="delim", type="text", disabled=True),
                ),
                Horizontal(
                    Label("Skip rows", classes="label_switch"),
                    Input(
                        id="skip_input",
                        disabled=True,
                        validators=[Number(minimum=0, maximum=100)],
                    ),
                ),
                Horizontal(
                    Label("Header", classes="label_switch"),
                    Switch(id="header", disabled=True),
                    classes="switch_container",
                ),
                Horizontal(
                    Label("Normalize names", classes="label_switch"),
                    Switch(id="normalize_names", disabled=True),
                    classes="switch_container",
                ),
                # TODO names
                Rule(),
                Horizontal(
                    Button(
                        "Edit", id="btn_edit", variant="warning", classes="btn_edit"
                    ),
                    Button(
                        "Save",
                        id="btn_save",
                        variant="success",
                        disabled=True,
                        classes="btn_save",
                    ),
                ),
                id="configuration_data",
                classes="configuration_data",
            ),
        )

    def on_mount(self):

        self.query_one("#configuration_data", Vertical).border_title = "Configuration"

    def _render(self):

        flist = [(v, v) for v in os.listdir(self._dir)]
        # update option list
        conflist = self.query_one("#conf_list", Select)
        conflist.clear()
        conflist.set_options(options=flist)
        # highlight option list
        conflist.value = self._filename

        # load conf
        data = SettingsDB.load_file(os.path.join(self._dir, self._filename))

        # delimitator
        delim = self.query_one("#delim", Input)
        delim.value = data.conf.delim

        # header
        header = self.query_one("#header", Switch)
        header.value = data.conf.header

        # skip rows
        delim = self.query_one("#skip_input", Input)
        delim.value = str(data.conf.skip)

        # normalize names
        normalize = self.query_one("#normalize_names", Switch)
        normalize.value = data.conf.normalize_names

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        if str(event.value) == "Select.BLANK":
            return

        if event.value != self._filename:
            self._filename = event.value
            self._render()

    def _enable_input(self, elem_id: str):
        self.query_one(f"#{elem_id}", Input).disabled = False

    def _enable_switch(self, elem_id: str):
        self.query_one(f"#{elem_id}", Switch).disabled = False

    def _disable_input(self, elem_id: str):
        self.query_one(f"#{elem_id}", Input).disabled = True

    def _disable_switch(self, elem_id: str):
        self.query_one(f"#{elem_id}", Switch).disabled = True

    def _toggle_button(self, btn_id: str):
        btn = self.query_one(f"#{btn_id}", Button)
        btn.disabled = not btn.disabled

    def load_filename(self, filename: str, dir: str):
        self._filename = filename
        self._origianl_fname = filename
        self._dir = dir
        self._render()

    def _get_conf_data(self):
        new_data = SettingsDB()
        new_data.conf.header = self.query_one("#header", Switch).value
        new_data.conf.skip = self.query_one("#skip_input", Input).value
        new_data.conf.delim = self.query_one("#delim", Input).value
        new_data.conf.normalize_names = self.query_one("#normalize_names", Switch).value

        new_data.save_file(str(os.path.join(self._dir, self._filename)))
        self.notify("Saved")

        self._disable_form()
        # reload confs
        self._render()

    def _get_new_filename(self, new_fname):
        if new_fname == "":
            return

        self._filename = new_fname
        self._get_conf_data()

    def _save_content(self):

        if self._filename == os.path.split(ANADI_DEFAULT_CONF_FILE)[1]:
            # ask for a new name
            self.app.push_screen(
                SaveAsModal(ANADI_CUSTOM_CONFS), self._get_new_filename
            )
        else:
            self._get_conf_data()

    @on(Button.Pressed, "#change_conf_file_btn")
    def on_click_apply_btn(self):
        # update original filename
        self._original_fname = self.query_one("#conf_list", Select).value
        # update csv <-> conf association and
        # send a message to the App
        self.post_message(EventCSVConfAssociationChanged(self._filename))

        self._render()

    @on(Button.Pressed, "#btn_edit")
    def on_edit_btn_click(self):
        # enable Save button
        self._toggle_button("btn_save")

        # disable Edit button
        self._toggle_button("btn_edit")

        # enable input and switch elements
        self._enable_input("skip_input")
        self._enable_input("delim")

        self._enable_switch("normalize_names")
        self._enable_switch("header")

    def _disable_form(self):
        # disable Save button
        self._toggle_button("btn_save")

        # enable Edit button
        self._toggle_button("btn_edit")

        # enable input and switch elements
        self._disable_input("skip_input")
        self._disable_input("delim")

        self._disable_switch("normalize_names")
        self._disable_switch("header")

    @on(Button.Pressed, "#btn_save")
    def on_save_btn_click(self):

        try:
            self._save_content()
        except Exception as ex:
            with open("error.log", "w") as errfile:
                errfile.write(f"{ex}")

            self.notify(f"{ex}", severity="error")
