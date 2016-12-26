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
RpqLua = RpqLua()
RpqLua.setRedisConnection(r);
RpqLua.loadSource('../../src/redis-priority-queue.lua');
queue = RpqLua.register();

# RpqQueue instance
RpqQueue = RpqQueue()

# Set LUA Script
RpqQueue.setLuaScript(queue)

# Set queue name
RpqQueue.setqueueName('simple_queue')

# Pop an item / some items

print ('* pop (one):')
item = RpqQueue.popOne()
if item:
    print (item);
else:
    print ('Queue is empty');

print ('* pop (one, ascending):')
item = RpqQueue.popOne('asc')
if item:
    print (item);
else:
    print ('Queue is empty');

print ('* pop (many):')
items = RpqQueue.popMany('desc', 5)
if items:
    listItems(items)
else:
    print ('Queue is empty');
