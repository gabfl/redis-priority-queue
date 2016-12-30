<?php
use RedisPriorityQueue as RPQ;

// Requires
require_once(__DIR__.'/../lib/Redis.php');

// Vars
$host = '127.0.0.1';
$port = 6379;
$auth = '';
$dbnum = 0;

// Redis instance
$r = new RPQ\Redis($host, $port, $auth, $dbnum);
// var_dump($r->getConnection());
