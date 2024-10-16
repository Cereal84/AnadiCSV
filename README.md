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
Anadi.

Syntax: anadi [-c|h|-d|-f|-q|-t]
options:
h         Print this Help.
c  PATH       Specify the settings file location.
d  PATH       Specify the data location. The default is the current directory.
f  FILE_PATH  Specify the filename which you want to know the schema or execute a query
q  SQL_QUERY  Specify the query you want to execute on file specified by -f FILE_PATH
t             Show the table schema of the CSV file passed via -f FILE_PATH
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

**[NOTE]** The table name is the filename without extension.

#### Run query via terminal

It is possible to run a query for a specific CSV file directly via terminal/shell 
without the TUI (Textual User Interface).

```shell
anadi -f measurements.csv -q "SELECT * FROM measurements"
+------------+-------------+------------+--------------+
|    date    | temperature | wind_speed | air_pressure |
+------------+-------------+------------+--------------+
| 2024-01-01 |      16     |    0.0     |     1000     |
| 2024-01-02 |      15     |    0.0     |     1010     |
| 2024-01-03 |      16     |    0.1     |     1020     |
+------------+-------------+------------+--------------+
```

#### See CSV File Table schema via terminal

```shell
anadi -f measurements.csv -t
Tablename: measurements
+--------------+-------------+------+------+---------+-------+
| column_name  | column_type | null | key  | default | extra |
+--------------+-------------+------+------+---------+-------+
|     date     |     DATE    | YES  | None |   None  |  None |
| temperature  |    BIGINT   | YES  | None |   None  |  None |
|  wind_speed  |    DOUBLE   | YES  | None |   None  |  None |
| air_pressure |    BIGINT   | YES  | None |   None  |  None |
+--------------+-------------+------+------+---------+-------+
```


## UI

### Conf Tab

In this tab you can set how to interprete the CSV file.


#### CSV Delimitator

Is the character used to separate the data inside the CSV.

Default: *,*.

#### Skip

The Skip option allows you to skip a number of rows at the beginning of your data series. This is useful for omitting metadata or comments that may precede the actual data.
Specify the lines that you want to skip. For example, if you set Skip to 2, the first two rows will be ignored when processing the data set.

Default: *0*.

##### Example

Imagine you have the following CSV file

```csv
1,2,3,4
01-01-2024,16,0,1000
02-01-2024,15,0,1010
03-01-2024,16,0.1,1020
```
Setting _Skip_ as 1 Anadi to ignore the first line.


#### Header

Specify if the CSV file has a header (the row in which you can see each column name).
When you enable this option. The first row of your data is considered the header. The next row will contain the actual data.

Default: *enabled*.

##### Example

Suppose to have the following CSV file

```csv
Date,Temperature,Wind Speed,Air Pressure
01-01-2024,16,0,1000
02-01-2024,15,0,1010
03-01-2024,16,0.1,1020
```

Enabling the _Header_ option Anadi knows that the first line is the header and so construct the columns name using those
information.
So the columns name are:
 - Date
 - Temperature
 - Wind Speed
 - Ait Pressure.

Instead if you have the following one


```csv
1,2,3,4
Date,Temperature,Wind Speed,Air Pressure
01-01-2024,16,0,1000
02-01-2024,15,0,1010
03-01-2024,16,0.1,1020
```

You need to use both _Skip_ equal to 1 and enabling _Header_ option.

#### Normalize name

The Normalize Names option normalizes the column naming format. This helps ensure consistency and prevents problems caused by naming variations (e.g. spaces, case sensitivity).
When activated This option converts all column names to a specific format (such as lowercase letters, underscores instead of spaces) to facilitate data management and analysis.

Default: *enabled*

##### Example

Suppose to have the following CSV file

```csv
1,2,3,4
Date,Temperature,Wind Speed,Air Pressure
01-01-2024,16,0,1000
02-01-2024,15,0,1010
03-01-2024,16,0.1,1020
```

If you use the last conf and enable the _normalize name_ option the column name will be in lower case and the spaces are replaced with underscores, they will be:

 - date
 - temperature
 - wind_speed
 - air_pressure.
 

## How Contribute

Please read [CONTRIBUTING.md](CONTRIBUTING.md) file.
