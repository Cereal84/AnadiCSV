# AnadiCSV

This tool aims to allow the user to interrogate a csv file using SQL language.

## How to install

Use a virtual env:

```shell
$ cd anadi_tui

$ python3.11 -m venv venv
$ source venv/bin/activate

$ poetry install
```

## How to use

### Help

```shell
$ anadi -h
usage: AnadiCSV [-h] -d DIR

Handle csv file using SQL language

options:
  -h, --help         show this help message and exit
  -d DIR, --dir DIR  CSV file dir
```

### How to run

After enabling the virtual environment use:

```shell
anadi -d DATA_DIR
```
