# redis-priority-queue: PHP client

PHP client for redis-priority-queue.

## Requirements

 - PHP >= 7.1
 - [phpredis](https://github.com/phpredis/phpredis)

## Sample use

```php
<?php
use RedisPriorityQueue as RQP;

// Requires
require_once(__DIR__.'/../lib/Lua.php');
require_once(__DIR__.'/../lib/Queue.php');
require_once(__DIR__.'/../lib/Redis.php');

// Create a Redis instance
$r = new RQP\Redis($host, $port, $auth, $dbnum);

// Create Queue instance with Redis connection
$q = new RQP\Queue($r->getConnection());

// Set queue name
$q->setQueueName('sample_queue');

// Push an item in the queue
$res = $q->push('item');
echo $res;

// Pop an item from the queue
$res = $q->pop();
echo json_encode($res)."\n";
```

## More examples

More examples are available in [/tests](tests/).
