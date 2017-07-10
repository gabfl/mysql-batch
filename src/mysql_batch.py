#!/usr/bin/env python3

# Author: Gabriel Bordeaux (gabfl)
# Github: https://github.com/gabfl/mysql-batch-update
# Compatible with python 2.7 & 3

import sys, time
import pymysql.cursors, argparse

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-H", "--host", default="127.0.0.1",
                    help="MySQL server host")
parser.add_argument("-P", "--port", type=int, default=3306,
                    help="MySQL server port")
parser.add_argument("-U", "--user", required = True,
                    help="MySQL user")
parser.add_argument("-p", "--password", default='',
                    help="MySQL password")
parser.add_argument("-d", "--database", required = True,
                    help="MySQL database name")
parser.add_argument("-t", "--table", required = True,
                    help="MySQL table")
parser.add_argument("-id", "--primary_key", default='id',
                    help="Name of the primary key column")
parser.add_argument("-w", "--where", required = True,
                    help="Select WHERE clause")
parser.add_argument("-s", "--set",
                    help="Update SET clause")
parser.add_argument("-rbz", "--read_batch_size", type=int, default = 10000,
                    help="Select batch size")
parser.add_argument("-wbz", "--write_batch_size", type=int, default = 50,
                    help="Update/delete batch size")
parser.add_argument("-S", "--sleep", type=float, default = 0.00,
                    help="Sleep after each batch")
parser.add_argument("-a", "--action", default = 'update', choices=['update', 'delete'],
                    help="Action ('update' or 'delete')")
parser.add_argument("-n", "--no_confirm", action='store_true',
                    help="Don't ask for confirmation before to run the write queries")
args = parser.parse_args()

# Make sure we have a SET clause for updates
if args.action == 'update' and args.set is None:
    print ("Error: argument -s/--set is required for updates.");
    sys.exit();

def updateBatch(ids):
    global confirmedWrite

    """Update a batch of rows"""

    # Leave if ids is empty
    if not ids or len(ids) == 0:
        return None;

    # Prepare update
    print('* Updating %i rows...' % len(ids))
    sql = "UPDATE " + args.table + " SET " + args.set + " WHERE {0} IN (".format(args.primary_key) + ', '.join([str(x) for x in ids]) + ")"
    print ("   query: " + sql)

    if confirmedWrite or query_yes_no("* Start updating?"):
        # Switch confirmedWrite skip the question for the next update
        confirmedWrite = True

        # Execute query
        runQuery(sql)
    else: # answered "no"
        print ("Error: Update declined.");
        sys.exit();

def deleteBatch(ids):
    global confirmedWrite

    """Delete a batch of rows"""

    # Leave if ids is empty
    if not ids or len(ids) == 0:
        return None;

    # Prepare delete
    print('* Deleting %i rows...' % len(ids))
    sql = "DELETE FROM " + args.table + " WHERE {0} IN (".format(args.primary_key) + ', '.join([str(x) for x in ids]) + ")"
    print ("   query: " + sql)

    if confirmedWrite or query_yes_no("* Start deleting?"):
        # Switch confirmedWrite skip the question for the next delete
        confirmedWrite = True

        # Execute query
        runQuery(sql)
    else: # answered "no"
        print ("Error: Delete declined.");
        sys.exit();

def runQuery(sql):
    """Execute a write query"""

    # Execute query
    with connection.cursor() as cursorUpd:
        cursorUpd.execute(sql)
        connection.commit()

    # Optional Sleep
    if args.sleep > 0:
        time.sleep(args.sleep)

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".

    (thanks https://code.activestate.com/recipes/577058/)
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)

        # Get user choice with python 2.7 retro-compatibility
        if sys.version_info >= (3,0):
            # Python 3
            # print ("python >= 3");
            choice = input().lower()
        else:
            # Python 2.7 retro-compatibility
            # print ("python 2.7");
            choice = raw_input().lower()

        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def main():
    global confirmedWrite, connection

    # Connect to the database
    try:
        connection = pymysql.connect(host = args.host,
                                     user = args.user,
                                     port = args.port,
                                     password = args.password,
                                     db = args.database,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
    except:
        print ("Error: MySQL connection failed.");
        sys.exit();

    try:
        # confirmedWrite default value
        confirmedWrite = False
        if args.no_confirm:
            confirmedWrite = True

        with connection.cursor() as cursor:
            # Default vars
            minId = 0

            while 1: # Infinite loop, will be broken by sys.exit()
                # Get rows to modify
                print("* Selecting data...")
                sql = "SELECT {0} as id FROM ".format(args.primary_key) + args.table + " WHERE " + args.where + " AND {0} > %s ORDER BY {1} LIMIT %s".format(args.primary_key, args.primary_key)
                print ("   query: " + sql % (minId, args.read_batch_size))
                cursor.execute(sql, (minId, args.read_batch_size))

                # Row count
                count = cursor.rowcount

                # No more rows
                if count == 0:
                    print ("* No more rows to modify!");
                    sys.exit();

                # Loop thru rows
                print("* Preparing to modify %s rows..." % count)
                ids = []
                for result in cursor:
                    # Append ID to batch
                    ids.append(result.get('id'));
                    # print(result)

                    # Minimum ID for future select
                    minId = result.get('id');

                    # Process write when batch size if reached
                    if len(ids) >= args.write_batch_size:
                        if args.action == 'delete':
                            # Process delete
                            deleteBatch(ids)
                        else :
                            # Process update
                            updateBatch(ids)

                        # Reset ids
                        ids = []

                # Process final batch
                if ids and len(ids) >= 0:
                    if args.action == 'delete':
                        # Process delete
                        deleteBatch(ids)
                    else :
                        # Process update
                        updateBatch(ids)
    except SystemExit:
        print("* Program exited")
    #except:
    #    print("Unexpected error:", sys.exc_info()[0])
    finally:
        connection.close()

if __name__ == '__main__':
    main()
