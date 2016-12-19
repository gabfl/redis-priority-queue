# redis-priority-queue

redis-priority-queue is a simple work queue similar to [Redis lists](https://redis.io/commands#list) with the following added features:

 - An item can be added with a priority (between -9007199254740992 and 9007199254740992)
 - Multiple items can be popped from the queue at the same time
 - A queue monitoring tool to easily see how many items are in each queue

redis-priority-queue is based on [Redis sorted sets](https://redis.io/commands#sorted_set) and all sorted sets commands can be used alongside this project.

## Basic usage

### Bash example

```
-- Generic
redis-cli --eval src/redis-priority-queue.lua null null , [push|pop|peek|count] my_list (arg1, arg2...)

-- Push an item
redis-cli --eval src/redis-priority-queue.lua null null , push my_super_list my_item

-- Pop an item
redis-cli --eval src/redis-priority-queue.lua null null , pop my_super_list my_item
```

## `push`: Push an item in a queue

### Usage
`push my_list item [(int) priority (default: 100)]`

### Examples

```
-- Push an item with the default priority (100)
push my_super_list my_item

-- Push an item with a priority of 200
push my_super_list my_item 200
```

### Return

Output is similar to [ZADD](https://redis.io/commands/zadd)

## `pop`: Pop an item from the queue

### Usage
`pop my_list [(string) asc/desc (default: 'asc')] [(int) numer_of_items (default: 1')]`

### Examples

```
-- Pop 1 item ordered by ascending priority
pop my_super_list

-- Pop 1 item ordered by descending priority
pop my_super_list desc

-- Pop 5 items ordered by ascending priority
pop my_super_list asc 5
```

### Return

Output is similar to [ZRANGEBYSCORE](https://redis.io/commands/zrangebyscore)

## `peek`: View a set of items from the list
Aliases: `list`, `view`

### Usage

Same as `pop` but items are not removed from the list.

## `count`: Count items in a queue

Alias: `size`

### Usage

`count my_list [(int) priority_min] [(int) priority_max]`

### Examples

```
-- Count all items from the list
count my_super_list

-- Count all items with a priority between 1 and 1110
count my_super_list 1 1110
```

### Return

Output is similar to [ZCOUNT](https://redis.io/commands/zcount)

## Queue monitoring

The queues can be easily monitored with the Python script `src/queue_monitor.py`

To use the queue monitor, you need to ensure python is installed and use the following command to add the required packages:
`pip install prettytable argparse redis`

### Usage example

```
./src/queue_monitor.py -H [host] -p [port] (-a [auth] -n [dbnum])
+-------------------+-------+-----------------+----------------+
| Queue Name        | Total | Priority <= 100 | Priority > 100 |
+-------------------+-------+-----------------+----------------+
| late_fees_pending |    44 |              12 |             32 |
| new_books         |   223 |             123 |            100 |
| book_recycle      |    13 |              13 |              0 |
| book_orders       |   112 |              56 |             56 |
| book_returns      | 1,144 |           1,120 |             24 |
+-------------------+-------+-----------------+----------------+
```

## Clients

 - [PHP client](clients/php/)
 - [Python client](clients/python/)
