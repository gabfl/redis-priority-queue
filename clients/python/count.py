#!/usr/bin/env python3

# Packages
import redis
from lib.RpqQueue import RpqQueue
from lib.RpqLua import RpqLua
from utils.redis_vars import *

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

# Get queue size

print ('* count (total):')
print (RpqQueue.count())

print ('* count (0 >= priority >= 100):')
print (RpqQueue.count(0, 100))

print ('* count (priority > 100):')
print (RpqQueue.count(101))