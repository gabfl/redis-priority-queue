#!/usr/bin/python

import sys, getopt, redis, argparse
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
args = parser.parse_args()

# Redis connection
r = redis.StrictRedis(host=args.host, port=args.port, db=args.dbnum, password=args.auth)

# Get queues
queueNames = r.smembers('rpq|names')

# Table titles
titles=['Queue Name', 'Total', 'Priority <= 100', 'Priority > 100']

# Create table
t = PrettyTable(titles)

# Column alignment
t.align['Queue Name'] = "l" # Left align queue names
t.align['Total'] = "r" # Right align numbers
t.align['Priority <= 100'] = "r" # Right align numbers
t.align['Priority > 100'] = "r" # Right align numbers

# Add a row par queue
for queueName in queueNames:
    # Get counts
    countA = r.zcount(queueName, '-inf', '+inf')
    countB = r.zcount(queueName, '-inf', 100)
    countC = r.zcount(queueName, 101, '+inf')

    # Add row
    t.add_row([queueName, '{0:,}'.format(countA), '{0:,}'.format(countB), '{0:,}'.format(countC)])

# Print table
print t