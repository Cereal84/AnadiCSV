# AnadiCSV

This tool aims to allow the user to interrogate a csv file using SQL language.

**[NOTE]** At the moment we support Docker only containers.

## How to install


```shell
$ cd AnadiCSV

$ ./install.sh

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

By default anadi use te current folder to find CSV files

```shell
anadi
```

if your files are in a different location use *-d* options


```shell
anadi -d DATA_DIR
```
