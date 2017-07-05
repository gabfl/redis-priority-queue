-- redis-priority-queue
-- Author: Gabriel Bordeaux (gabfl)
-- Github: https://github.com/gabfl/redis-priority-queue
-- Version: 1.0.4
-- (can only be used in 3.2+)

-- Get mandatory vars
local action = ARGV[1];
local queueName = ARGV[2];

-- Define misc vars
local queueMonitor = 'rpq|names'

-- returns true if empty or null
-- http://stackoverflow.com/a/19667498/50501
local function isempty(s)
  return s == nil or s == '' or type(s) == 'userdata'
end

-- Making sure required fields are not nil
assert(not isempty(action), 'ERR1: Action is missing')
assert(not isempty(queueName), 'ERR2: Queue name is missing')

if action == 'push'
then
    -- debug
    redis.debug('Push new item');

    -- Define vars
    local item = ARGV[3];
    local priority = ARGV[4] or 100;

    -- debug
    redis.debug('...queue name -> '..queueName);
    redis.debug('...item -> '..item);
    redis.debug('...priority -> '..priority);

    -- Making sure required fields are not nil
    assert(not isempty(item), 'ERR5: Item is missing')

    -- Add queue name to the set of queues (for monitoring purpose)
    redis.call("SADD", queueMonitor, queueName)

    -- Add item to queue
    return redis.call('ZADD', queueName, 'NX', priority, item)
elseif action == 'pop' or action == 'peek' or action == 'list' or action == 'view'
then
    -- debug
    redis.debug('Pop/peek items');

    -- Define vars
    local orderBY = ARGV[3] or 'desc';
    local itemsCount = ARGV[4] or 1;

    -- Sorting vars
    local rangeMethod = '';
    local fromMin = '';
    local toMax = '';
    if orderBY == 'asc' -- asc sorting
    then
        rangeMethod = 'ZRANGEBYSCORE';
        fromMin = '-inf';
        toMax ='+inf';
    elseif orderBY == 'desc' -- desc sorting
    then
        rangeMethod = 'ZREVRANGEBYSCORE';
        fromMin = '+inf';
        toMax ='-inf';
    else
        error('ERR4: Invalid sorting order.')
    end

    -- Retrieve items
    local popped = redis.call(rangeMethod, queueName, fromMin, toMax, 'LIMIT', 0, itemsCount)

    -- If items are popped from the list
    if action == 'pop'
    then
        -- Rotate thru popped items
        if popped then
            for _,item in ipairs(popped) do
                -- debug
                redis.debug('...popped item -> '..item);

                -- Remove item
                redis.call('ZREM', queueName, item)
            end
        end
    end

    -- If the queue is empty, remove from the set of queues
    if next(popped) == nil
    then
        redis.call('SREM', queueMonitor, queueName)
    end

    return popped;
elseif action == 'size' or action == 'count'
then
    -- debug
    redis.debug('Get queue size');

    -- Define vars
    local fromMin = ARGV[3] or '-inf';
    local toMax = ARGV[4] or '+inf';

    -- debug
    redis.debug('...queue name -> '..queueName);
    redis.debug('...from priotity # -> '..fromMin);
    redis.debug('...to priotity # -> '..toMax);

    -- return queue count
    local count = redis.call('ZCOUNT', queueName, fromMin, toMax)

    -- If the queue is empty, remove from the set of queues
    if count == 0
    then
        redis.call('SREM', queueMonitor, queueName)
    end

    return count;
else
    error('ERR3: Invalid action.')
end
