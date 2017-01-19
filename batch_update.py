#!/usr/bin/env python3

# Author: Gabriel Bordeaux (gabfl)
# Github: https://github.com/gabfl/mysql-batch-update
# Version: 1.0
# Compatible with python 3

import pymysql.cursors, sys, argparse, time

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
parser.add_argument("-id", "--id", default='id',
                    help="Name of the ID column")
parser.add_argument("-w", "--where", required = True,
                    help="Select WHERE clause")
parser.add_argument("-u", "--update", required = True,
                    help="Update SET clause")
parser.add_argument("-sbz", "--select_batch_size", type=int, default = 1000,
                    help="Select batch size")
parser.add_argument("-ubz", "--update_batch_size", type=int, default = 50,
                    help="Update batch size")
parser.add_argument("-s", "--sleep", type=float, default = 0.00,
                    help="Sleep after an update")
args = parser.parse_args()

def update_batch(ids):
    global confirmedUpdate

    """Update a batch of rows"""

    # Leave if ids is empty
    if not ids or len(ids) == 0:
        return None;

    # Prepare update
    print('* Updating %i rows...' % len(ids))
    sql = "UPDATE " + args.table + " SET " + args.update + " WHERE {0} IN (".format(args.id) + ', '.join([str(x) for x in ids]) + ")"
    print ("   query: " + sql)

    if confirmedUpdate or query_yes_no("* Start updating?"):
        # Switch confirmedUpdate skip the question for the next update
        confirmedUpdate = True

        # Execute query
        cursor.execute(sql)
        connection.commit()

        # Optional Sleep
        if args.sleep > 0:
            time.sleep(args.sleep)
    else: # answered "no"
        print ("Error: Update declined.");
        sys.exit();


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
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
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

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
    with connection.cursor() as cursor:
        minId = 0
        confirmedUpdate = False
        while 1: # Infinite loop, will be broken by sys.exit()
            # Get rows to update
            print("* Selecting data...")
            sql = "SELECT {0} as id FROM ".format(args.id) + args.table + " WHERE " + args.where + " AND {0} > %s ORDER BY {1} LIMIT %s".format(args.id, args.id)
            print ("   query: " + sql % (minId, args.select_batch_size))
            cursor.execute(sql, (minId, args.select_batch_size))

            # No more rows
            if cursor.rowcount == 0:
                print ("* No more rows to update!");
                sys.exit();

            # Loop thru rows
            ids = []
            for result in cursor:
                # Append ID to batch
                ids.append(result.get('id'));
                # print(result)

                # Update minimum ID for future select
                minId = result.get('id');

                # Process update when batch size if reached
                if len(ids) >= args.update_batch_size:
                    # Process update
                    update_batch(ids)

                    # Reset ids
                    ids = []

            # Process final batch
            if ids and len(ids) >= 0:
                # Process update
                update_batch(ids)
except SystemExit:
    print("* Program exited")
#except:
#    print("* Unexpected error:", sys.exc_info()[0])
finally:
    connection.close()
