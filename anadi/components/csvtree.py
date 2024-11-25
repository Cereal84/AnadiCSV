from pathlib import Path
from typing import Iterable

from textual.widgets import DirectoryTree, SelectionList

import os

class CSVTree(DirectoryTree):
    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if path.name.endswith(".csv")]


class CSVMultiSelect(SelectionList[str]):

    def load_files(self, path: str):
        # iterate throught the directories  
        for fname in os.listdir(path):
            if os.path.isfile(fname) and fname.endswith(".csv"):
                self.add_option((fname, os.path.join(path, fname)))
