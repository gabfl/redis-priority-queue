# redis-priority-queue

redis-priority-queue is a simple work queue similar to [Redis lists](https://redis.io/commands#list) with the following added features:

 - An item can be added with a priority (between -9007199254740992 and 9007199254740992)
 - Queues are automatically de-duplicated (duplicate items are voided when pushing them)
 - Multiple items can be popped from the queue at the same time
 - A [queue monitoring tool](#queue-monitoring) to easily see how many items are in each queue

redis-priority-queue is based on [Redis sorted sets](https://redis.io/commands#sorted_set) and all sorted sets commands can be used alongside this project.

## Clients

 - [Python client](clients/python/)
 - [PHP client](clients/php/)

## Basic usage

### Bash example

```
-- Generic
redis-cli --eval src/redis-priority-queue.lua null null , [push|pop|peek|count] my_list (arg1, arg2...)

-- Push an item
redis-cli --eval src/redis-priority-queue.lua null null , push my_super_list my_item

-- Pop an item
redis-cli --eval src/redis-priority-queue.lua null null , pop my_super_list
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
`pop my_list [(string) asc/desc (default: 'desc')] [(int) numer_of_items (default: 1')]`

### Examples

```
-- Pop 1 item ordered by descending priority
pop my_super_list

-- Pop 1 item ordered by ascending priority
pop my_super_list asc

-- Pop 5 items ordered by descending priority
pop my_super_list desc 5
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

To use the queue monitor, you need to ensure python is installed and use the following command:
```
# Installation
pip3 install rpq

# Usage
rpq_monitor
```

### Usage example

```
# Basic usage
rpq_monitor -H [host] -p [port] (-a [auth] -n [dbnum])
+-------------------+-------+-----------+----------+
| Queue name        | Total | Up to 100 | From 101 |
+-------------------+-------+-----------+----------+
| book_orders       |    44 |        12 |       32 |
| book_recycle      |   223 |       123 |      100 |
| book_returns      |    13 |        13 |        0 |
| late_fees_pending |   112 |        56 |       56 |
| new_books         | 1,144 |     1,120 |       24 |
+-------------------+-------+-----------+----------+

# Specify your own groups
rpq_monitor -H [host] -p [port] (-a [auth] -n [dbnum]) -s "[[0, 1000], [1001, 2000], [2001, 3000]]"
+-------------------+-------+------------+----------------+----------------+
| Queue name        | Total | 0 to 1,000 | 1,001 to 2,000 | 2,001 to 3,000 |
+-------------------+-------+------------+----------------+----------------+
| book_orders       |    44 |         24 |              9 |             11 |
| book_recycle      |   223 |        127 |             40 |             56 |
| book_returns      |    13 |         13 |              0 |              0 |
| late_fees_pending |   112 |         58 |             13 |             41 |
| new_books         | 1,144 |      1,142 |              2 |              0 |
+-------------------+-------+------------+----------------+----------------+
```
