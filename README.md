# mysql-batch-update

Updating a large amount of rows in MySQL will create locks that will paralyze other queries running in parallel.

This tool will run updated in small batches to prevent table-level and row-level locking (with InnoDB). If a large number of rows has to be updated, it is also possible to limit the number of rows selected at once.

## Requirements

 - Python 3
 - pymysql (`pip3 install pymysql`)
 - argparse (`pip3 install argparse`)

## Example

You can run this example with the schema available in [sample_table/schema.sql](sample_table/schema.sql)

The following example will be identical to the following update:

```sql
UPDATE test_update SET date = NOW() WHERE number > 0.2 AND date is NULL;
```

To re-create this update 20 rows at a time:

```bash
python3 batch_update.py --host localhost \
                        --user root \
                        --password ***** \
                        --database "test" \
                        --table "test_update" \
                        --update_batch_size 20 \
                        --where "number > 0.2 AND date IS NULL" \
                        --update "date = NOW()"
```

Output sample:

```bash
* Selecting data...
   query: SELECT id as id FROM test_update WHERE number > 0.2 AND date IS NULL AND id > 0 ORDER BY id LIMIT 1000
* Updating 20 rows...
   query: UPDATE test_update SET date = NOW() WHERE id IN (1, 2, 4, 5, 6, 7, 9, 10, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 24, 26)
* Start updating? [Y/n]
* Selecting data...
   query: SELECT id as id FROM test_update WHERE number > 0.2 AND date IS NULL AND id > 26 ORDER BY id LIMIT 1000
* Updating 20 rows...
   query: UPDATE test_update SET date = NOW() WHERE id IN (27, 28, 30, 32, 34, 35, 38, 40, 42, 43, 45, 47, 48, 49, 50, 51, 52, 55, 56, 57)
* Selecting data...
   query: SELECT id as id FROM test_update WHERE number > 0.2 AND date IS NULL AND id > 57 ORDER BY id LIMIT 1000
* Updating 20 rows...
   query: UPDATE test_update SET date = NOW() WHERE id IN (58, 59, 60, 61, 62, 63, 64, 66, 67, 69, 70, 71, 72, 73, 74, 76, 78, 79, 81, 83)
* Selecting data...
   query: SELECT id as id FROM test_update WHERE number > 0.2 AND date IS NULL AND id > 83 ORDER BY id LIMIT 1000
* Updating 13 rows...
   query: UPDATE test_update SET date = NOW() WHERE id IN (84, 85, 86, 87, 88, 90, 91, 94, 95, 96, 97, 98, 99)
* Selecting data...
   query: SELECT id as id FROM test_update WHERE number > 0.2 AND date IS NULL AND id > 99 ORDER BY id LIMIT 1000
* No more rows to update!
* Program exited
```

## Usage

```bash
usage: batch_update.py [-h] [-H HOST] [-P PORT] -U USER [-p PASSWORD] -d
                       DATABASE -t TABLE [-id ID] -w WHERE -u UPDATE
                       [-sbz SELECT_BATCH_SIZE] [-ubz UPDATE_BATCH_SIZE]
                       [-s SLEEP]

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
  -id ID, --id ID       Name of the ID column
  -w WHERE, --where WHERE
                        Select WHERE clause
  -u UPDATE, --update UPDATE
                        Update SET clause
  -sbz SELECT_BATCH_SIZE, --select_batch_size SELECT_BATCH_SIZE
                        Select batch size
  -ubz UPDATE_BATCH_SIZE, --update_batch_size UPDATE_BATCH_SIZE
                        Update batch size
  -s SLEEP, --sleep SLEEP
                        Sleep after an update
```

## License

This program is under MIT license ([view license](LICENSE)).
