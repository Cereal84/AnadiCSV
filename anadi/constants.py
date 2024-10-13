import os

ANADI_PATH = os.path.abspath(os.path.expanduser("~/.config/anadi"))
ANADI_CONF_FILE = f"{ANADI_PATH}/conf.json"
ANADI_HISTORY_FILE = f"{ANADI_PATH}/history.json"
ANADI_CUSTOM_CONFS = f"{ANADI_PATH}/confs/"
ANADI_DEFAULT_CONF_FILE = f"{ANADI_CUSTOM_CONFS}/default"
ANADI_RESULTS_DIR = f"{ANADI_PATH}/results/"
