<?php
use RedisPriorityQueue as RQP;

// Requires
require_once(__DIR__.'/../utils/redis_instance.php');
require_once(__DIR__.'/../utils/const.php');
require_once(__DIR__.'/../lib/Lua.php');
require_once(__DIR__.'/../lib/Queue.php');

// Create Queue instance with Redis connection
$q = new RQP\Queue($r->getConnection());

// Set queue name
$q->setQueueName(QUEUE_NAME);

// Run
echo "* push (without priority):\n";
$res = $q->push(mt_rand());
echo $res."\n";

// Run
echo "* push (with priority):\n";
$res = $q->push(mt_rand(), PRIORITY);
echo $res."\n";
