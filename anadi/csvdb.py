import inspect
from typing import List

import duckdb

from anadi.models.confs import SettingsDB
from anadi.models.query_result import QueryResult


class CSVDB:

    def __init__(self):
        self._filename = ""
        self._conf = None
        self._db_conn = None 
        self._table_name = ""

    def table_name(self) -> str:
        return self._table_name

    def load(self, filename: str, conf: SettingsDB):
        self._filename = filename
        self._table_name = conf.table_name
        self._conf = conf.conf
        self._import_csv()

    def _import_csv(self):
        # CREATE DB
        self._db_conn = duckdb.connect(database=':memory:')
        # create table and import CSV
        # TODO add columns_type for the schema
        from_section = f"""FROM read_csv('{self._filename}',
                           header={self._conf.header},
                           delim='{self._conf.delim}',
                           skip={self._conf.skip},
                           names={self._conf.names},
                           normalize_names={self._conf.normalize_names})"""
        self._db_conn.sql(f"CREATE TABLE {self._table_name} AS {from_section}")

    def exec_show_schema(self):
        res = self._db_conn.sql(f"DESCRIBE TABLE '{self._table_name}'")
        return self._gen_query_result(res)

    def exec_get_columns_name(self) -> List:
        res = self._db_conn.sql(f"DESCRIBE TABLE '{self._table_name}'") 
        col_name = []
        for row in res.fetchall():
             col_name.append(row[0])

        return col_name 

    def exec_raw_sql(self, sql: str):
        """split the query and put the FROM section"""
        res = self._db_conn.sql(sql)
        return self._gen_query_result(res)

    def raw_sql(self, sql: str):
        return self.exec_raw_sql(sql)

    def get_columns_name(self):
        return self.exec_get_columns_name()

    def get_schema(self):
        return self.exec_show_schema()

    def _gen_query_result(self, res) -> QueryResult:
        header = res.columns
        data = res.fetchall()

        return QueryResult(header=header, rows=data)

    def get_antenna_gain_list(self) -> QueryResult:
        res = self._db_conn.sql(f"SELECT DISTINCT(ant_gain_db) FROM '{self._table_name}'")
        return self._gen_query_result(res)

    def get_method_list(self):
        methods_list = [ method[0].replace('exec_', '') for method in inspect.getmembers(self, predicate=inspect.ismethod) if method[0].startswith('exec_') ]

        return methods_list

