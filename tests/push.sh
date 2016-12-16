#!/bin/bash

source set_vars.sh

redis-cli -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_AUTH --eval ../src/redis-priority-queue.lua null null , push $QUEUE_NAME $ITEM_NAME $PRIORITY
