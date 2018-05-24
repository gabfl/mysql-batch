#!/usr/bin/env python3

# Author: Gabriel Bordeaux (gabfl)
# Github: https://github.com/gabfl/mysql-batch
# Compatible with python 2.7 & 3

import sys
import time
import pymysql.cursors
import argparse


def update_batch(ids, table, set_, primary_key='id'):
    """
        Update a batch of rows
    """

    global confirmed_write

    # Leave if ids is empty
    if not ids or len(ids) == 0:
        return None

    # Prepare update
    print('* Updating %i rows...' % len(ids))
    sql = "UPDATE " + table + " SET " + set_ + \
        " WHERE {0} IN (".format(primary_key) + \
        ', '.join([str(x) for x in ids]) + ")"
    print("   query: " + sql)

    if confirmed_write or query_yes_no("* Start updating?"):
        # Switch confirmed_write skip the question for the next update
        confirmed_write = True

        # Execute query
        run_query(sql)
    else:  # answered "no"
        print("Error: Update declined.")
        sys.exit()

    return True


def delete_batch(ids, table, primary_key='id'):
    """
        Delete a batch of rows
    """

    global confirmed_write

    # Leave if ids is empty
    if not ids or len(ids) == 0:
        return None

    # Prepare delete
    print('* Deleting %i rows...' % len(ids))
    sql = "DELETE FROM " + table + \
        " WHERE {0} IN (".format(primary_key) + \
        ', '.join([str(x) for x in ids]) + ")"
    print("   query: " + sql)

    if confirmed_write or query_yes_no("* Start deleting?"):
        # Switch confirmed_write skip the question for the next delete
        confirmed_write = True

        # Execute query
        run_query(sql)
    else:  # answered "no"
        print("Error: Delete declined.")
        sys.exit()

    return True


def run_query(sql, sleep=0):
    """Execute a write query"""

    # Execute query
    with connection.cursor() as cursorUpd:
        cursorUpd.execute(sql)
        connection.commit()

    # Optional Sleep
    if sleep > 0:
        time.sleep(sleep)

    return True


def get_input():
    """
        Get user input
    """

    # Get user choice with python 2.7 retro-compatibility
    if sys.version_info >= (3, 0):
        # Python 3
        # print ("python >= 3");
        return input().lower()
    else:
        # Python 2.7 retro-compatibility
        # print ("python 2.7");
        return raw_input().lower()


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
        choice = get_input()

        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def connect(host, user, port, password, database):
    """
        Connect to a MySQL database
    """

    # Connect to the database
    try:
        return pymysql.connect(host=host,
                               user=user,
                               port=port,
                               password=password,
                               db=database,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
    except Exception:
        raise RuntimeError('Error: MySQL connection failed.')


def execute(host, user, port, password, database, action, table, where, set_=None, no_confirm=False, primary_key='id', read_batch_size=10000, write_batch_size=50):
    global confirmed_write, connection

    # Make sure we have a SET clause for updates
    if action == 'update' and set_ is None:
        raise RuntimeError('Error: argument -s/--set is required for updates.')

    # Connect to the database
    connection = connect(host, user, port, password, database)

    try:
        # confirmed_write default value
        confirmed_write = False
        if no_confirm:
            confirmed_write = True

        with connection.cursor() as cursor:
            # Default vars
            min_id = 0

            while 1:  # Infinite loop, will be broken by sys.exit()
                # Get rows to modify
                print("* Selecting data...")
                sql = "SELECT {0} as id FROM ".format(primary_key) + table + " WHERE " + where + \
                    " AND {0} > %s ORDER BY {1} LIMIT %s".format(
                        primary_key, primary_key)
                print("   query: " + sql % (min_id, read_batch_size))
                cursor.execute(sql, (min_id, read_batch_size))

                # Row count
                count = cursor.rowcount

                # No more rows
                if count == 0:
                    print("* No more rows to modify!")
                    sys.exit()

                # Loop thru rows
                print("* Preparing to modify %s rows..." % count)
                ids = []
                for result in cursor:
                    # Append ID to batch
                    ids.append(result.get('id'))
                    # print(result)

                    # Minimum ID for future select
                    min_id = result.get('id')

                    # Process write when batch size if reached
                    if len(ids) >= write_batch_size:
                        if action == 'delete':
                            # Process delete
                            delete_batch(ids, table, primary_key)
                        else:
                            # Process update
                            update_batch(ids, table, set_, primary_key)

                        # Reset ids
                        ids = []

                # Process final batch
                if ids and len(ids) >= 0:
                    if action == 'delete':
                        # Process delete
                        delete_batch(ids, table, primary_key)
                    else:
                        # Process update
                        update_batch(ids, table, set_, primary_key)
    except SystemExit:
        print("* Program exited")
    # except:
    #    print("Unexpected error:", sys.exc_info()[0])
    finally:
        connection.close()

    return True


def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", default="127.0.0.1",
                        help="MySQL server host")
    parser.add_argument("-P", "--port", type=int, default=3306,
                        help="MySQL server port")
    parser.add_argument("-U", "--user", required=True,
                        help="MySQL user")
    parser.add_argument("-p", "--password", default='',
                        help="MySQL password")
    parser.add_argument("-d", "--database", required=True,
                        help="MySQL database name")
    parser.add_argument("-t", "--table", required=True,
                        help="MySQL table")
    parser.add_argument("-id", "--primary_key", default='id',
                        help="Name of the primary key column")
    parser.add_argument("-w", "--where", required=True,
                        help="Select WHERE clause")
    parser.add_argument("-s", "--set",
                        help="Update SET clause")
    parser.add_argument("-rbz", "--read_batch_size", type=int, default=10000,
                        help="Select batch size")
    parser.add_argument("-wbz", "--write_batch_size", type=int, default=50,
                        help="Update/delete batch size")
    parser.add_argument("-S", "--sleep", type=float, default=0.00,
                        help="Sleep after each batch")
    parser.add_argument("-a", "--action", default='update', choices=['update', 'delete'],
                        help="Action ('update' or 'delete')")
    parser.add_argument("-n", "--no_confirm", action='store_true',
                        help="Don't ask for confirmation before to run the write queries")
    args = parser.parse_args()

    execute(host=args.host,
            user=args.user,
            port=args.port,
            password=args.password,
            database=args.database,
            action=args.action,
            table=args.table,
            where=args.where,
            set_=args.set,
            no_confirm=args.no_confirm,
            primary_key=args.primary_key,
            read_batch_size=args.read_batch_size,
            write_batch_size=args.write_batch_size
            )


if __name__ == '__main__':
    main()
