
import argparse

from anadi.app import AnadiApp
from anadi.constants import *
from anadi.csvdb import CSVDB
from anadi.models.confs import SettingsApp, SettingsDB

parser = argparse.ArgumentParser(prog="AnadiCSV", description="Handle CVS file using SQL language")
parser.add_argument("-d", "--dir", type=str, help="CSV file dir", required=True)
parser.add_argument("-q", "--query", type=str, help="SQL query to execute", required=False)


def run():
    args = parser.parse_args()

    try:
        app = AnadiApp()
        app.init(args.dir, os.path.abspath(os.path.expanduser(ANADI_CONF_FILE)))
        if args.query:
            csvdb = CSVDB()
            csvdb.load(args.dir,SettingsDB())
            result = csvdb.raw_sql(args.query)
            print(result)
        else:
            app.run()
    except Exception as ex:
        print(ex)
        with open("error.log", 'w') as errfile:
            errfile.write(f"{ex}")


if __name__ == "__main__":
    run()
