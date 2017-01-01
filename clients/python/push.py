#!/usr/bin/env python3

# Packages
import redis, random
from lib.RpqQueue import RpqQueue
from lib.RpqLua import RpqLua
from utils.redis_vars import *

def generateRandom():
    '''Helper: get a random integer'''
    return random.randint(1, 100000);

def getItem():
    '''Helper: generate item name'''
    return 'item_' + str(generateRandom());

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

# Push an item

print ('* push (without priority):')
item = getItem() # Item we will push to the queue
print ('Pushing item "%s" to the queue' % (item))
print (RpqQueue.push(item))

print ('* push (with priority):')
item = getItem() # Item we will push to the queue
print ('Pushing item "%s" to the queue' % (item))
print (RpqQueue.push(item, 1000))