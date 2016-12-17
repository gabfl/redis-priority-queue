<?php
namespace RedisPriorityQueue;

class Queue extends Lua
{
    // Private
    private $_queueName;
    private $_args = []; // Array of arguments

    /**
     * __construct function.
     *
     * @access public
     * @param mixed $connection
     * @param string $luaFilePath (default: __DIR__.'/../../../src/redis-priority-queue.lua')
     * @return void
     */
    public function __construct($connection, string $luaFilePath = __DIR__.'/../../../src/redis-priority-queue.lua')
    {
        // Set Redis connection
        $this->setConnection($connection);

        // Set lua path
        $this->setpath($luaFilePath);
    }

    /**
     * prepareArgs function.
     *
     * @access private
     * @param string $action
     * @param array $args
     * @return bool
     */
    private function prepareArgs(string $action, array $args): bool
    {
        return $this->setArgs(
            array_merge(
                [$action], // action
                [$this->_queueName], // queue name
                $args
            )
        );
    }

    /**
     * setQueueName function.
     *
     * @access public
     * @param string $queueName
     * @return void
     */
    public function setQueueName(string $queueName)
    {
        $this->_queueName = $queueName;
    }

    /**
     * push function.
     *
     * @access public
     * @param string $item
     * @param int $priority (default: null)
     * @return int
     */
    public function push(string $item, int $priority = null): int
    {
        // Append args
        $args = [$item];
        if (!is_null($priority)) {
            array_push($args, $priority);
        }

        // Set args
        $this->prepareArgs('push', $args);

        return $this->run();
    }

    /**
     * pop function.
     *
     * @access public
     * @param string $orderBy (default: 'asc')
     * @param int $numberOfItems (default: 1)
     * @return misc
     */
    public function pop(string $orderBy = 'asc', int $numberOfItems = 1)
    {
        // Set args
        $this->prepareArgs('pop', [$orderBy, $numberOfItems]);

        return $this->run();
    }

    /**
     * peek function.
     *
     * @access public
     * @param string $orderBy (default: 'asc')
     * @param int $numberOfItems (default: 1)
     * @return misc
     */
    public function peek(string $orderBy = 'asc', int $numberOfItems = 1)
    {
        // Set args
        $this->prepareArgs('peek', [$orderBy, $numberOfItems]);

        return $this->run();
    }

    /**
     * count function.
     *
     * @access public
     * @param int $priorityMin (default: null)
     * @param int $priorityMax (default: null)
     * @return int
     */
    public function count(int $priorityMin = null, int $priorityMax = null): int
    {
        // Append args
        $args = [];
        if (!is_null($priorityMin)) {
            array_push($args, $priorityMin);
        }
        if (!is_null($priorityMin) && !is_null($priorityMax)) {
            array_push($args, $priorityMax);
        }

        // Set args
        $this->prepareArgs('count', $args);

        return $this->run();
    }
}
