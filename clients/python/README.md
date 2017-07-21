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
from rpq.RpqQueue import RpqQueue

# Redis instance
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password='')

# RpqQueue
queue = RpqQueue(r, 'simple_queue')

# Pop an item / some items

print ('* push:')
res = queue.push('test_item')
print (res)

print ('* pop:')
item = queue.popOne()
if item:
    print (item)
else:
    print ('Queue is empty')
```

## More examples

More examples are available in this folder.
