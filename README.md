# AnadiCSV

This tool aims to allow the user to interrogate a csv file using SQL language.

**[NOTE]** At the moment we support Docker only containers in Linux Debian/Ubuntu platform.


![screenshot](images/screenshots/screenshot1.png)


## How to install


```shell
$ cd AnadiCSV

$ ./install.sh

```

## How to use

### Help

```shell
$ ./anadi.sh -h
usage: AnadiCSV [-h] -d DIR

Handle csv file using SQL language

options:
  -h, --help         show this help message and exit
  -d DIR, --dir DIR  CSV file dir
```

### How to run

By default anadi use te current folder to find CSV files

```shell
./anadi.sh
```

if your files are in a different location use *-d* options


```shell
./anadi.sh -d DATA_DIR
```
