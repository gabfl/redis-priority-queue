#!/usr/bin/env python3

# Packages
import redis
from rpq import RpqQueue
from rpq import RpqLua


def listItems(items):
    '''Helper to print items'''
    for item in items:
        print (item)


# Redis instance
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password='')

# Load LUA Script
RpqLua = RpqLua.RpqLua(r)
queue = RpqLua.register()

# RpqQueue instance
RpqQueue = RpqQueue.RpqQueue(queue)

# Set queue name
RpqQueue.setqueueName('simple_queue')

# Pop an item / some items

print ('* pop (one):')
item = RpqQueue.popOne()
if item:
    print (item)
else:
    print ('Queue is empty')

print ('* pop (one, ascending):')
item = RpqQueue.popOne('asc')
if item:
    print (item)
else:
    print ('Queue is empty')

print ('* pop (many):')
items = RpqQueue.popMany('desc', 5)
if items:
    listItems(items)
else:
    print ('Queue is empty')
