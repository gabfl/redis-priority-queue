<?php
use RedisPriorityQueue as RPQ;

// Requires
require_once(__DIR__.'/../utils/redis_instance.php');
require_once(__DIR__.'/../utils/const.php');
require_once(__DIR__.'/../lib/Lua.php');
require_once(__DIR__.'/../lib/Queue.php');

// Create Queue instance with Redis connection
$q = new RPQ\Queue($r->getConnection());

// Set queue name
$q->setQueueName(QUEUE_NAME);

// Run
echo "* count (total):\n";
$res = $q->count();
echo $res."\n";

// Run
echo "* count (0 >= priority >= 100):\n";
$res = $q->count(0, 100);
echo $res."\n";

// Run
echo "* count (priority > 100):\n";
$res = $q->count(101);
echo $res."\n";
