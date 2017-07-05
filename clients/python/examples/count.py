#!/usr/bin/env python3

# Packages
import redis
from rpq import RpqQueue
from rpq import RpqLua

# Redis instance
r = redis.StrictRedis(host = '127.0.0.1', port = 6379, db = 0, password = '')

# Load LUA Script
RpqLua = RpqLua.RpqLua(r);
queue = RpqLua.register();

# RpqQueue instance
RpqQueue = RpqQueue.RpqQueue(queue);

# Set queue name
RpqQueue.setqueueName('simple_queue')

# Get queue size

print ('* count (total):')
print (RpqQueue.count())

print ('* count (0 >= priority >= 100):')
print (RpqQueue.count(0, 100))

print ('* count (priority > 100):')
print (RpqQueue.count(101))
