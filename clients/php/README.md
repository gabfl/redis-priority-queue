# redis-priority-queue: PHP client

PHP client for redis-priority-queue.

## Requirements

 - PHP >= 7.1
 - [phpredis](https://github.com/phpredis/phpredis)

## Sample use

```php
<?php
use RedisPriorityQueue as RPQ;

// Requires
require_once('lib/Lua.php');
require_once('lib/Queue.php');
require_once('lib/Redis.php');

// Create a Redis instance
$r = new RPQ\Redis($host, $port, $auth, $dbnum);

// Create Queue instance with Redis connection
$q = new RPQ\Queue($r->getConnection());

// Set queue name
$q->setQueueName('sample_queue');

// Push an item in the queue
$res = $q->push('item');
echo "* Push an item:\n";
echo $res."\n";

// Pop an item from the queue
$res = $q->popOne();
echo "* Pop an item:\n";
echo json_encode($res)."\n";
```

## More examples

More examples are available in [/tests](tests/).
