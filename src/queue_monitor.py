#!/usr/bin/env python3

# redis-priority-queue -> queue monitor
# Author: Gabriel Bordeaux (gabfl)
# Github: https://github.com/gabfl/redis-priority-queue
# Compatible with python 2.7 & 3

import redis
import argparse
import json
from prettytable import PrettyTable

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-H", "--host", default="127.0.0.1",
                    help="Redis server host")
parser.add_argument("-p", "--port", type=int, default=6379,
                    help="Redis server port")
parser.add_argument("-a", "--auth",
                    help="Redis server authentification")
parser.add_argument("-n", "--dbnum", type=int, default=0,
                    help="Redis server database number")
parser.add_argument("-s", "--sort_groups",
                    help="Sort groups", type=json.loads)
args = parser.parse_args()

# Global vars
t = None
r = None


def setSortGroups(sortGroups=None):
    """
        Return the sorting groups, either user defined or from the default list
    """

    if sortGroups is None:  # Default groups
        return [('-inf', '+inf'), ('-inf', 100), (101, '+inf')]
    else:
        sortGroups.insert(0, ('-inf', '+inf'))
        return sortGroups


def getCount(queueName, min, max):
    """
        Fetches set count from Redis
    """

    global r

    return r.zcount(queueName, min, max)


def getColumnTitle(min, max):
    """
        Human readable column titles
    """

    if str(min) == '-inf' and str(max) == '+inf':
        return 'Total'
    elif str(min) == '-inf':
        return 'Up to ' + '{0:,}'.format(max);
    elif str(max) == '+inf':
        return 'From ' + '{0:,}'.format(min);
    elif min == max:
        return '{0:,}'.format(min);
    else:
        return '{0:,}'.format(min) + ' to ' + '{0:,}'.format(max);


def setColumnAlign(titles):
    """
        Set PrettyTable column alignment
    """

    global t

    for i, title in enumerate(titles):
        if i == 0:  # First column (title)
            t.align[title] = 'l'  # Left
        else:  # Any other column
            t.align[title] = 'r'  # Right


def main():
    global t, r

    # Redis connection
    try:
        r = redis.StrictRedis(host=args.host, port=args.port, db=args.dbnum, password=args.auth)
    except Exception as e:
        import sys

        print('Redis error: %s' % (e))
        sys.exit()

    # Sort groups
    sortGroups = setSortGroups(args.sort_groups)

    # Column titles (queue name, then a column per sorting group)
    titles = ['Queue name']
    titles.extend([getColumnTitle(sortGroup[0], sortGroup[1]) for sortGroup in sortGroups])

    # Create table
    t = PrettyTable(titles)
    setColumnAlign(titles)

    # Get queues
    try:
        queueNames = r.smembers('rpq|names')
    except Exception as e:
        import sys

        print('Redis error: %s' % (e))
        sys.exit()

    # Add a row par queue
    for queueName in sorted(queueNames):
        # Get row
        row = [queueName.decode("utf-8")]
        row.extend(['{0:,}'.format(getCount(queueName, sortGroup[0], sortGroup[1])) for sortGroup in sortGroups]);

        # Add row
        t.add_row(row)

    # Print table
    print (t)


if __name__ == '__main__':
    main()
