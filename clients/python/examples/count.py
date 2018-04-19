#!/usr/bin/env python3

# Packages
import redis
from rpq.RpqQueue import RpqQueue

# Redis instance
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password='')

# RpqQueue
queue = RpqQueue(r, 'simple_queue')

# Get queue size

print('* count (total):')
print(queue.count())

print('* count (0 >= priority >= 100):')
print(queue.count(0, 100))

print('* count (priority > 100):')
print(queue.count(101))
