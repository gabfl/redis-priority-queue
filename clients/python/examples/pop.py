#!/usr/bin/env python3

# Packages
import redis
from rpq.RpqQueue import RpqQueue


def listItems(items):
    '''Helper to print items'''
    for item in items:
        print (item)


# Redis instance
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password='')

# RpqQueue
queue = RpqQueue(r, 'simple_queue')

# Pop an item / some items

print ('* pop (one):')
item = queue.popOne()
if item:
    print (item)
else:
    print ('Queue is empty')

print ('* pop (one, ascending):')
item = queue.popOne('asc')
if item:
    print (item)
else:
    print ('Queue is empty')

print ('* pop (many):')
items = queue.popMany('desc', 5)
if items:
    listItems(items)
else:
    print ('Queue is empty')
