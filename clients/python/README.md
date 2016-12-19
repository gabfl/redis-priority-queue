# redis-priority-queue: Python client

Python client for redis-priority-queue.

## Requirements

 - Python 3
 - redis python package (`pip install redis`)

## Sample use

```python
#!/usr/bin/env python3

# Packages
import redis
from lib.RpqQueue import RpqQueue
from lib.RpqLua import RpqLua

# Redis instance
r = redis.StrictRedis(host='127.0.0.1', port=6483, db=0, password='97e4cda4851539dbb33a891fdd714499501a4dc8')

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

print ('* push:')
res = RpqQueue.push('test_item')
print (res);

print ('* pop:')
items = RpqQueue.pop()
print (items[0]);

```

## More examples

More examples are available in this folder.
