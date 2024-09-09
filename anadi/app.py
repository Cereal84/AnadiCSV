"""
    This file contains the App class.

    __author__: Alessandro Pischedda alessandro.pischedda@gmail.com
"""

import json
import re

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Rule
from textual.widgets import Button, DataTable, TextArea, Label
from textual.containers import Vertical


from anadi.csvdb import CSVDB
from anadi.constants import *
from anadi.components.data_container import DataContainer
from anadi.components.conf_editor import EventCSVConfAssociationChanged
from anadi.components.csvtree import CSVTree
from anadi.modals.quit import QuitAppModal
from anadi.modals.history import HistoryCmdModal
from anadi.models.confs import SettingsApp, SettingsDB


class AnadiApp(App):

    CSS_PATH = "layouts/horizontal_layout.tcss"

    BINDINGS = [
                ("s", "show_tab('sql_tab')", "Show to SQL Tab"),
                ("c", "show_tab('conf_tab')", "Show Conf Tab"),
                ("h", "show_history", "Show SQL History"),
                ("q", "quit_app", "Quit")]

    TITLE = "AnadiCSV"

    def init(self, csv_dir: str, conffile: str):
        self._csv_dir = csv_dir
        self._conf_file = conffile

        self._check_init_fs()

        self._conf = SettingsApp.load_file(conffile)
        self._csv_selected = ""
        self._csvdb = CSVDB()
        self._cmd_history = []
        self._load_history()

    def _check_init_fs(self):

        if not os.path.exists(ANADI_PATH):
            os.makedirs(ANADI_PATH)

        if not os.path.exists(self._conf_file):
            SettingsApp.save_default(self._conf_file)

        if not os.path.exists(ANADI_CUSTOM_CONFS):
            os.makedirs(ANADI_CUSTOM_CONFS)

        if not os.path.exists(ANADI_RESULTS_DIR):
            os.makedirs(ANADI_RESULTS_DIR)


        if not os.path.exists(ANADI_DEFAULT_CONF_FILE):
            SettingsDB.save_default(ANADI_DEFAULT_CONF_FILE)

    def _load_history(self):
       if not os.path.isfile(self._conf.history.filename):
           return

       with open(self._conf.history.filename, 'r') as historyfile:
            self._cmd_history = json.load(historyfile)

    def _get_conf_file_for_csv(self) -> str:
        # from file get custom DBConf
        db_conf_file = self._conf.default_conf
        for rule, conf_file in self._conf.custom_confs.items():
            p = re.compile(r"{}".format(rule))
            match = p.search(self._csv_selected)
            if match:
                db_conf_file = conf_file 
                break
        return db_conf_file

    def _conn_to_db(self):
       db_conf = SettingsDB.load_file(self._get_conf_file_for_csv())
       self._csvdb.load(self._csv_selected, db_conf)


    @on(EventCSVConfAssociationChanged)
    def reload_csv(self, message: EventCSVConfAssociationChanged) -> None:
        # update csv <-> conf association
        self._conf.custom_confs[self._csv_selected] = os.path.join(ANADI_CUSTOM_CONFS, message.confname)
        self._conf.save_file(self._conf_file)
        self._update_side_bar_info()


    def on_mount(self) -> None:
        # write settings tab

        data_container = self.query_one("#data_container", DataContainer)

        csv_tree = self.query_one("#flist", CSVTree)
        csv_tree.border_title = "CSV Files"

        schema = self.query_one("#table_schema", DataTable)
        schema.border_title = "Table Schema"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Vertical(
             CSVTree(self._csv_dir, id="flist", classes="box_csv_tree"),
             Rule(),
             Label("Table: None", id="table_name"),
             Rule(), 
             DataTable(id="table_schema", classes="box_schema", zebra_stripes=True),
             classes="sidebar"
        )
        yield DataContainer("", classes="box", id="data_container")

        yield Footer()

    def action_quit_app(self):
        self.push_screen(QuitAppModal())

    def action_show_history(self):
        def get_selected_sql(sql: str | None) -> None:
            """Called when QuitScreen is dismissed."""
            if sql is not None:
                # copy sql into SQL Code editor
                data_container = self.query_one("#data_container", DataContainer)
                data_container.copy_query_to_editor(sql)

        self.push_screen(HistoryCmdModal(self._cmd_history),  get_selected_sql)

    def action_show_tab(self, tab: str) -> None:
        """Switch to a new tab."""
        data_container = self.query_one("#data_container", DataContainer)
        data_container.change_tab(tab)

    def _render_db_conffile(self):

        db_conf_file = self._get_conf_file_for_csv()
        conf_tab = self.query_one("#data_container", DataContainer)
        conf_tab.render_conf_db(db_conf_file)


    def _update_side_bar_info(self):

        self._render_db_conffile()
        self._conn_to_db()

        # show table name
        table_name = self.query_one("#table_name", Label)
        table_name.update(f"Table: {self._csvdb.table_name()}")

        # show schema
        schema_elem = self.query_one("#table_schema", DataTable)
        schema_elem.clear(columns=True)
        schema_data = self._csvdb.get_schema() 
        schema_elem.add_column(schema_data.header[0])
        schema_elem.add_column(schema_data.header[1])
        for row in schema_data.rows:
            d = (row[0], row[1])
            schema_elem.add_row(*d)     

        schema_elem.sort()


    def on_directory_tree_file_selected(
        self, event: CSVTree.FileSelected
    ) -> None:
        """Called when the user click a file in the directory tree."""
        event.stop()
        if self._csv_selected == str(event.path):
            return

        self._csv_selected = str(event.path)
        self._update_side_bar_info()

        data_container = self.query_one("#data_container", DataContainer)
        data_container.enable_sql_editor()
        
    @on(Button.Pressed, "#btn_run")
    def onclick_btn_run(self):
        """ handle Run button click """

        if self._csv_selected == "":
            self.notify(f"No CSV file selected", severity="error")
            return

        query = self.query_one("#sql", TextArea).text
        if query == "":
            self.notify("Empty query", severity="error") 
            return

        try:

            res = self._csvdb.exec_raw_sql(query)
            table = self.query_one("#sql_data", DataTable)
            table.clear(columns=True)
            for h in res.header:
                table.add_column(h)

            table.add_rows(res.rows)

            # enable Export button
            export_btn = self.query_one("#btn_export", Button)
            export_btn.disabled = False


            # Store query into the SQL History 
            if len(self._cmd_history) == self._conf.history.size:
                self._cmd_history.pop(0)
            self._cmd_history.append(query)
            with open(self._conf.history.filename, 'w') as historyfile:
                historyfile.write(json.dumps(self._cmd_history))
 

        except Exception as ex:
            with open("error.log", 'w') as errfile:
                errfile.write(f"{ex}")
            self.notify(f"{ex}",  severity="error")

       

