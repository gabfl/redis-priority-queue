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
echo "* pop (one):\n";
$res = $q->popOne();
echo $res."\n";

// Run
echo "* pop (one, descending):\n";
$res = $q->popOne('desc');
echo $res."\n";

// Run
echo "* pop (many):\n";
$res = $q->popMany('asc', MULTIPLE_ITEMS_COUNT);
echo json_encode($res)."\n";
