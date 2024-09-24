
import argparse

from anadi.app import AnadiApp
from anadi.constants import *


parser = argparse.ArgumentParser(prog="AnadiCSV", description="Handle CVS file using SQL language")
parser.add_argument("-d", "--dir", type=str, help="CSV file dir", required=True)



def run():
    args = parser.parse_args()

    try:
        app = AnadiApp()
        app.init(args.dir, os.path.abspath(os.path.expanduser(ANADI_CONF_FILE)))
        app.run()
    except Exception as ex:
        print(ex)
        with open("error.log", 'w') as errfile:
            errfile.write(f"{ex}")


if __name__ == "__main__":
    run()