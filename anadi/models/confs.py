import json
import os
from typing import List, Optional

from pydantic import BaseModel, validator

from anadi.constants import (
    ANADI_DEFAULT_CONF_FILE,
    ANADI_HISTORY_FILE,
    ANADI_RESULTS_DIR,
)


class HistoryConf(BaseModel):
    filename: Optional[str] = os.path.abspath(os.path.expanduser(ANADI_HISTORY_FILE))
    size: Optional[int] = 20


class SettingsApp(BaseModel):
    version: int = 1
    default_conf: str = os.path.abspath(os.path.expanduser(ANADI_DEFAULT_CONF_FILE))
    custom_confs: dict[str, str] = {}
    results_dir: str = ANADI_RESULTS_DIR
    history: HistoryConf = HistoryConf()

    @classmethod
    def check_file(cls, v: str):
        if not os.path.exists(v):
            raise RuntimeError(f"File '{v}' does not exists")

        if not os.path.isfile(v):
            raise RuntimeError(f"'{v}' is not a file")

    @validator("default_conf")
    def validate_default(cls, v):
        if v == "":
            return

        SettingsApp.check_file(v)
        return v

    @validator("custom_confs")
    def validate_rules(cls, v):
        for _, conf in v.items():
            SettingsApp.check_file(conf)
        return v

    @classmethod
    def load_file(cls, filename: str):
        conf = None
        with open(filename, "r") as conffile:
            data = json.load(conffile)
            conf = SettingsApp(**data)

        return conf

    @classmethod
    def load_str(cls, data: str):
        return SettingsApp(**json.loads(data))

    @classmethod
    def save_default(cls, conffile: str):
        with open(conffile, "w") as cfile:
            json.dump(SettingsApp().dict(), cfile)

    def save_file(self, conffile: str):
        with open(conffile, "w") as cfile:
            json.dump(self.dict(), cfile)


class ConfDuckDB(BaseModel):

    header: bool = True
    skip: int = 0
    normalize_names: bool = True
    delim: str = ","
    names: List[str] = []


class SettingsDB(BaseModel):

    table_name: str = "tablename"
    conf: ConfDuckDB = ConfDuckDB()

    @classmethod
    def load_file(cls, filename: str | None):
        if filename is None:
            return SettingsDB()

        conf = None
        with open(filename, "r") as conffile:
            data = json.load(conffile)
            conf = SettingsDB(**data)

        return conf

    @classmethod
    def load_str(cls, data: str):
        return SettingsDB(**json.loads(data))

    @classmethod
    def save_default(cls, conffile: str):
        with open(conffile, "w") as cfile:
            json.dump(SettingsDB().dict(), cfile)

    def save_file(self, conffile: str):
        with open(f"{conffile}", "w") as cfile:
            json.dump(self.dict(), cfile)
