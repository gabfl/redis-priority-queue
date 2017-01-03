#!/usr/bin/env python3

# redis-priority-queue -> queue monitor
# Author: Gabriel Bordeaux (gabfl)
# Github: https://github.com/gabfl/redis-priority-queue
# Compatible with python 2.7 & 3

import redis, argparse
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
parser.add_argument("-s", "--sort_groups", action='append', 
                    help="Sort groups")
args = parser.parse_args()

def setSortGroups(sortGroups = None):
    """Return the sorting groups, either user defined or from the default list"""
    if sortGroups is None: # Default groups
        return [('-inf', '+inf'), ('-inf', 100), (101, '+inf')];
    else:
        groups = [('-inf', '+inf')]; # Default mandatory group (Total)
        groups.extend([tuple(map(int, sortGroup.split('->'))) for sortGroup in sortGroups])
        return groups;

def getCount(queueName, min, max):
    """Fetches set count from Redis"""
    return r.zcount(queueName, min, max);

def getColumnTitle(min, max):
    """Human readable column titles"""
    if str(min) == '-inf' and str(max) == '+inf':
        return 'Total';
    elif str(min) == '-inf':
        return 'Up to ' + '{0:,}'.format(max);
    elif str(max) == '+inf':
        return 'From ' + '{0:,}'.format(min);
    else:
        return '{0:,}'.format(min) + ' to ' + '{0:,}'.format(max);

def setColumnAlign(titles):
    """Set PrettyTable column alignment"""
    global t;
    for i, title in enumerate(titles):
        if i == 0: # First column (title)
            t.align[title] = 'l'; # Left
        else: # Any other column
            t.align[title] = 'r'; # Right

# Redis connection
r = redis.StrictRedis(host=args.host, port=args.port, db=args.dbnum, password=args.auth)

# Sort groups
sortGroups = setSortGroups(args.sort_groups);

# Column titles (queue name, then a column per sorting group)
titles = ['Queue name'];
titles.extend([getColumnTitle(sortGroup[0], sortGroup[1]) for sortGroup in sortGroups]);

# Create table
t = PrettyTable(titles);
setColumnAlign(titles);

# Get queues
queueNames = r.smembers('rpq|names')

# Add a row par queue
for queueName in sorted(queueNames):
    # Get row
    row = [queueName.decode("utf-8")]
    row.extend(['{0:,}'.format(getCount(queueName, sortGroup[0], sortGroup[1])) for sortGroup in sortGroups]);

    # Add row
    t.add_row(row);

# Print table
print (t);
