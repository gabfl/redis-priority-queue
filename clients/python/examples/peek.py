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

# Peek in a queue

print ('* peek (one):')
item = RpqQueue.peekOne()
if item:
    print (item)
else:
    print ('Queue is empty')

print ('* peek (one, ascending):')
item = RpqQueue.peekOne('asc')
if item:
    print (item)
else:
    print ('Queue is empty')

print ('* peek (many):')
items = RpqQueue.peekMany('desc', 5)
if items:
    listItems(items)
else:
    print ('Queue is empty')
