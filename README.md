# mysql-batch

[![Build Status](https://travis-ci.org/gabfl/mysql-batch.svg?branch=master)](https://travis-ci.org/gabfl/mysql-batch)

Updating or deleting a large amount of rows in MySQL will create locks that will paralyze other queries running in parallel.

This tool will run UPDATE and DELETE queries in small batches to prevent table-level and row-level locking (with InnoDB). If a large number of rows has to be updated or deleted, it is also possible to limit the number of rows selected at once.

## Installation

```
pip3 install mysql_batch
```

## UPDATE example

You can run this example with the schema available in [sample_table/schema.sql](sample_table/schema.sql)

The following example will be identical to the following update:

```sql
UPDATE batch_test SET date = NOW() WHERE number > 0.2 AND date is NULL;
```

This is the equivalent to process this update with batches of 20 rows:

```bash
mysql_batch --host localhost \
            --user root \
            --password secret_password \
            --database "test" \
            --table "batch_test" \
            --write_batch_size 20 \
            --where "number > 0.2 AND date IS NULL" \
            --set "date = NOW()"
```

Output sample:

```bash
* Selecting data...
   query: SELECT id as id FROM batch_test WHERE number > 0.2 AND date IS NULL AND id > 0 ORDER BY id LIMIT 1000
* Preparing to modify 83 rows...
* Updating 20 rows...
   query: UPDATE batch_test SET date = NOW() WHERE id IN (1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22)
* Start updating? [Y/n]
* Updating 20 rows...
   query: UPDATE batch_test SET date = NOW() WHERE id IN (23, 25, 26, 28, 29, 30, 31, 33, 35, 36, 37, 38, 39, 40, 42, 43, 44, 45, 46, 47)
* Updating 20 rows...
   query: UPDATE batch_test SET date = NOW() WHERE id IN (48, 49, 50, 51, 52, 53, 54, 55, 56, 58, 59, 60, 61, 63, 64, 65, 68, 69, 70, 71)
* Updating 20 rows...
   query: UPDATE batch_test SET date = NOW() WHERE id IN (72, 74, 75, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 88, 89, 90, 91, 92, 94, 95)
* Updating 3 rows...
   query: UPDATE batch_test SET date = NOW() WHERE id IN (97, 98, 100)
* Selecting data...
   query: SELECT id as id FROM batch_test WHERE number > 0.2 AND date IS NULL AND id > 100 ORDER BY id LIMIT 1000
* No more rows to modify!
* Program exited
```

## DELETE example

The following example will be identical to the following delete:

```sql
DELETE FROM batch_test WHERE number > 0.2 AND date is NULL;
```

This is the equivalent to process this delete with batches of 20 rows:

```bash
mysql_batch --host localhost \
            --user root \
            --password secret_password \
            --database "test" \
            --table "batch_test" \
            --write_batch_size 20 \
            --where "number > 0.2 AND date IS NULL" \
            --action "delete"
```

Output sample:

```bash
* Selecting data...
   query: SELECT id as id FROM batch_test WHERE number > 0.2 AND date IS NULL AND id > 0 ORDER BY id LIMIT 1000
* Preparing to modify 79 rows...
* Deleting 20 rows...
   query: DELETE FROM batch_test WHERE id IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 17, 19, 20, 21, 22, 23)
* Start deleting? [Y/n]
* Deleting 20 rows...
   query: DELETE FROM batch_test WHERE id IN (24, 25, 26, 28, 34, 35, 36, 37, 38, 39, 40, 41, 44, 45, 47, 48, 50, 51, 52, 53)
* Deleting 20 rows...
   query: DELETE FROM batch_test WHERE id IN (54, 56, 57, 58, 60, 61, 62, 63, 64, 65, 66, 67, 68, 70, 71, 72, 73, 74, 75, 76)
* Deleting 19 rows...
   query: DELETE FROM batch_test WHERE id IN (77, 78, 79, 80, 82, 83, 86, 87, 88, 89, 90, 91, 93, 94, 95, 96, 98, 99, 100)
* Selecting data...
   query: SELECT id as id FROM batch_test WHERE number > 0.2 AND date IS NULL AND id > 100 ORDER BY id LIMIT 1000
* No more rows to modify!
* Program exited
```

## Usage

```bash
usage: mysql_batch [-h] [-H HOST] [-P PORT] -U USER [-p PASSWORD] -d DATABASE
                   -t TABLE [-id PRIMARY_KEY] -w WHERE [-s SET]
                   [-rbz READ_BATCH_SIZE] [-wbz WRITE_BATCH_SIZE] [-S SLEEP]
                   [-a {update,delete}] [-n]

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  MySQL server host
  -P PORT, --port PORT  MySQL server port
  -U USER, --user USER  MySQL user
  -p PASSWORD, --password PASSWORD
                        MySQL password
  -d DATABASE, --database DATABASE
                        MySQL database name
  -t TABLE, --table TABLE
                        MySQL table
  -id PRIMARY_KEY, --primary_key PRIMARY_KEY
                        Name of the primary key column
  -w WHERE, --where WHERE
                        Select WHERE clause
  -s SET, --set SET     Update SET clause
  -rbz READ_BATCH_SIZE, --read_batch_size READ_BATCH_SIZE
                        Select batch size
  -wbz WRITE_BATCH_SIZE, --write_batch_size WRITE_BATCH_SIZE
                        Update/delete batch size
  -S SLEEP, --sleep SLEEP
                        Sleep after each batch
  -a {update,delete}, --action {update,delete}
                        Action ('update' or 'delete')
  -n, --no_confirm      Don't ask for confirmation before to run the write
                        queries
```

## License

This program is under MIT license ([view license](LICENSE)).
