from dataclasses import dataclass
from typing import List

from prettytable import PrettyTable


@dataclass
class QueryResult:

    header: List
    rows: List

    def __str__(self) -> str:
        table = PrettyTable()
        table.field_names = self.header
        for row in self.rows:
            table.add_row(row)

        return table.get_string()
