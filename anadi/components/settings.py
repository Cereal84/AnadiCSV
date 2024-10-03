from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label, Static

from anadi.constants import ANADI_CONF_FILE, ANADI_CUSTOM_CONFS
from anadi.models.confs import SettingsApp


class SettingsWidget(Static):

    DEFAULT_CSS = """

        SettingsWidget > Vertical {
            width: 100%;
        }

    """

    def __init__(self, id: str = None, name: str = None, classes: str = ""):
        self._settings = SettingsApp.load_file(ANADI_CONF_FILE)
        super().__init__(id=id, name=name, classes=classes)

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label(f"Default Conf: {self._settings.default_conf}")
            yield Label(f"Custom Confs: {ANADI_CUSTOM_CONFS}")
            yield Label(f"History file: {self._settings.history.filename}")
            yield Label(f"History limit: {self._settings.history.size}")
