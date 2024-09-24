# AnadiCSV

This tool aims to allow the user to interrogate a csv file using SQL language.

**[NOTE]** At the moment we support Docker only containers.


![screenshot](images/screenshots/screenshot1.png)


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

### Header

Description:
The header option allows you to specify the names of the columns in your dataset. This is especially helpful in making information readable and user-friendly.
Usage: When you enable this option. The first row of your data is considered the header. and the next row will contain the actual data.

### Skip

Description: The Skip option allows you to skip a number of rows at the beginning of your data series. This is useful for omitting metadata or comments that may precede the actual data.
Usage: Specify the lines that you want to skip. For example, if you set Skip to 2, the first two rows will be ignored when processing the data set.

### Normalize name

Description: The Normalize Names option normalizes the column naming format. This helps ensure consistency and prevents problems caused by naming variations (e.g. spaces, case sensitivity).
Usage: When activated This option converts all column names to a specific format (such as lowercase letters, underscores instead of spaces) to facilitate data management and analysis...