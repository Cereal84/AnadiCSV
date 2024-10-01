# AnadiCSV

This tool aims to allow the user to interrogate a csv file using SQL language.

## Supported Container Engine

   - Docker
   - Podman

## Supported O.S.

   - Linux
   - OSX


![screenshot](images/screenshots/screenshot1.png)


## How to install

Run the script *install.sh* with superuser privileges.

```shell
$ cd AnadiCSV

$ sudo ./install.sh

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

## UI

### Conf Tab

In this tab you can set how to interprete the csv file.

#### Tablename

**Description**
It is the name used in 'FROM' keyword inside the query to refer to the table.

**Default:** *tablename*.

#### CSV Delimitator

**Description**
Is the character used to separate the data inside the CSV.

**Default:** *,*

#### Skip

**Description**
The Skip option allows you to skip a number of rows at the beginning of your data series. This is useful for omitting metadata or comments that may precede the actual data.

**Usage**
Specify the lines that you want to skip. For example, if you set Skip to 2, the first two rows will be ignored when processing the data set.


#### Header

**Description**
Specify if the CSV file has a header (the row in which you can see each column name)

**Usage**
When you enable this option. The first row of your data is considered the header. The next row will contain the actual data.

**Default:** enabled

#### Normalize name

**Description**
The Normalize Names option normalizes the column naming format. This helps ensure consistency and prevents problems caused by naming variations (e.g. spaces, case sensitivity).

**Usage** When activated This option converts all column names to a specific format (such as lowercase letters, underscores instead of spaces) to facilitate data management and analysis.

**Default:** enabled

## How Contribute

Please read [CONTRIBUTING.md](CONTRIBUTING.md) file.
