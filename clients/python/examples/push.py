#!/usr/bin/env python3

# Packages
import redis
import random
from rpq import RpqQueue
from rpq import RpqLua


def generateRandom():
    '''Helper: get a random integer'''
    return random.randint(1, 100000)


def getItem():
    '''Helper: generate item name'''
    return 'item_' + str(generateRandom())


# Redis instance
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password='')

# Load LUA Script
RpqLua = RpqLua.RpqLua(r)
queue = RpqLua.register()

# RpqQueue instance
RpqQueue = RpqQueue.RpqQueue(queue)

# Set queue name
RpqQueue.setqueueName('simple_queue')

# Push an item

print ('* push (without priority):')
item = getItem()  # Item we will push to the queue
print ('Pushing item "%s" to the queue' % (item))
print (RpqQueue.push(item))

print ('* push (with priority):')
item = getItem()  # Item we will push to the queue
print ('Pushing item "%s" to the queue' % (item))
print (RpqQueue.push(item, 1000))
