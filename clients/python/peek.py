#!/usr/bin/env python3

# Packages
import redis
from lib.RpqQueue import RpqQueue
from lib.RpqLua import RpqLua
from utils.redis_vars import *

def listItems(items):
    '''Helper to print items'''
    for item in items:
        print (item);

# Redis instance
# !!! set Redis credentials into utils/redis_vars.py
r = redis.StrictRedis(host=rHost, port=rPort, db=rDbnum, password=rAuth)

# Load LUA Script
RpqLua = RpqLua(r, '../../src/redis-priority-queue.lua');
queue = RpqLua.register();

# RpqQueue instance
RpqQueue = RpqQueue(queue);

# Set queue name
RpqQueue.setqueueName('simple_queue')

# Peek in a queue

print ('* peek (one):')
item = RpqQueue.peekOne()
if item:
    print (item);
else:
    print ('Queue is empty');

print ('* peek (one, ascending):')
item = RpqQueue.peekOne('asc')
if item:
    print (item);
else:
    print ('Queue is empty');

print ('* peek (many):')
items = RpqQueue.peekMany('desc', 5)
if items:
    listItems(items)
else:
    print ('Queue is empty');
