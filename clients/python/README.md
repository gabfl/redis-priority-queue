# redis-priority-queue: Python client

Python client for redis-priority-queue.

## Requirements

 - Python 2.7 & 3

## Installation

```
pip3 install rpq
```

## Sample use

```python
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
RpqQueue = RpqQueue.RpqQueue(queue)

# Set queue name
RpqQueue.setqueueName('simple_queue')

# Pop an item / some items

print ('* push:')
res = RpqQueue.push('test_item')
print (res);

print ('* pop:')
item = RpqQueue.popOne()
if item:
    print (item);
else:
    print ('Queue is empty');
```

## More examples

More examples are available in this folder.
