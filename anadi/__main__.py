import argparse

from anadi.app import AnadiApp
from anadi.constants import *
from anadi.csvdb import CSVDB
from anadi.models.confs import SettingsApp, SettingsDB

parser = argparse.ArgumentParser(
    prog="AnadiCSV", description="Handle CVS file using SQL language"
)
parser.add_argument("-d", "--dir", type=str, help="CSV file dir", required=False)
parser.add_argument("-f", "--file", type=str, help="CSV file name", required=False)
parser.add_argument(
    "-q", "--query", type=str, help="SQL query to execute", required=False
)
parser.add_argument(
    "-t",
    "--tableschema",
    action="store_true",
    help="Show the schema of the file passed via --file",
)


def run():

    try:

        args, _ = parser.parse_known_args()

        if not args.dir and not args.file:
            raise ValueError("Error: Either --dir or --file must be provided.")
        if args.dir and args.file:
            raise ValueError("Error: Cannot user both --dir  and --file together")

        app = AnadiApp()
        if args.dir:
            app.init(args.dir, os.path.abspath(os.path.expanduser(ANADI_CONF_FILE)))
            app.run()
        elif args.file:
            csvdb = CSVDB()
            csvdb.load(args.file, SettingsDB())
            if args.query:
                result = csvdb.raw_sql(args.query)
                print(result)
            if args.tableschema:
                tablename = csvdb.table_name()
                schema = csvdb.get_schema()
                print(f"Tablename: {tablename}")
                print(schema)

    except Exception as ex:
        print(ex)
        with open("error.log", "w") as errfile:
            errfile.write(f"{ex}")


if __name__ == "__main__":
    run()
