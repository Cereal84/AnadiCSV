import os

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import (Button, DataTable, Label, Rule, Static,
                             TabbedContent, TabPane)

from anadi.components.conf_editor import ConfEditorWidget
from anadi.components.settings import SettingsWidget
from anadi.components.sql_editor import SQLEditor
from anadi.constants import ANADI_RESULTS_DIR
from anadi.modals.save_as import SaveAsModal
from anadi.models.confs import SettingsApp, SettingsDB


class DataContainer(Static):

    DEFAULT_CSS = """

        DataContainer > Vertical {
           height: auto;
        }

    """

    def compose(self) -> ComposeResult:

        with TabbedContent(initial="sql_tab", id="tabs"):
            with TabPane("SQL", id="sql_tab"):  # SQL tab
                yield Vertical(
                    DataTable(classes="data_table", id="sql_data", zebra_stripes=True),
                    Button(
                        "Save results",
                        id="btn_export",
                        classes="btn_export",
                        variant="success",
                        disabled=True,
                    ),
                    Rule(),
                    SQLEditor(id="sql_editor"),
                )

            with TabPane("Conf", id="conf_tab"):  # SettingsDB tab
                yield ConfEditorWidget(id="conf_db")

            with TabPane("Settings"):
                yield SettingsWidget()

    def _validate_settings(self, content_data: str):
        _ = SettingsApp.load_str(content_data)

    def _validate_db_conf(self, content_data: str):
        _ = SettingsDB.load_str(content_data)

    def render_conf_db(self, filename: str):
        conf_editor = self.query_one("#conf_db", ConfEditorWidget)
        filecomp = os.path.split(filename)
        conf_editor.load_filename(filecomp[1], filecomp[0])

    def change_tab(self, tab: str):
        self.query_one("#tabs", TabbedContent).active = tab

    def copy_query_to_editor(self, sql: str):
        sql_editor = self.query_one("#sql_editor", SQLEditor)
        sql_editor.render_sql_query(sql)

    def enable_sql_editor(self):
        sql_editor = self.query_one("#sql_editor", SQLEditor)
        sql_editor.enable()

    def _save_results(self, fname: str):
        fullname = os.path.join(ANADI_RESULTS_DIR, fname)

        data_table_obj = self.query_one("#sql_data", DataTable)

        header = [str(col.label.plain) for col in data_table_obj.ordered_columns]
        with open(fullname, "w") as savefile:
            savefile.write(f"{','.join(header)}\n")

            # write data
            for row_index in range(data_table_obj.row_count):
                row = data_table_obj.get_row_at(row_index)
                savefile.write(f"{','.join(map(str,row))}\n")

        self.notify(f"Data saved in '{fullname}'")

    @on(Button.Pressed, "#btn_export")
    def onclick_btn_export(self):
        """save data to file"""

        # open modal for filename
        self.app.push_screen(SaveAsModal(ANADI_RESULTS_DIR), self._save_results)
