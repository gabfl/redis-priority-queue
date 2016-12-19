#!/bin/bash

source set_vars.sh

for i in `seq 1 $MULTIPLE_ITEMS_COUNT`;
do
    redis-cli -h $REDIS_HOST -p $REDIS_PORT -a "$REDIS_AUTH" --eval ../src/redis-priority-queue.lua null null , push $QUEUE_NAME $ITEM_NAME"$i" $PRIORITY
done
