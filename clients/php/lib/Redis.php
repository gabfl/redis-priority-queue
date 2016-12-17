<?php
namespace RedisPriorityQueue;

class Redis
{
    // Private
    private $_host;
    private $_port;
    private $_auth;
    private $_dbnum;
    private $_connection;

    /**
     * __construct function.
     *
     * @access public
     * @param string $host (default: '127.0.0.1')
     * @param int $port (default: 6379)
     * @param string $auth (default: '')
     * @param int $dbnum (default: 0)
     * @return void
     */
    public function __construct(string $host = '127.0.0.1', int $port = 6379, string $auth = '', int $dbnum = 0)
    {
        // Reset connection
        $this->setConnection();

        // Set credentials
        $this->setCredentials($host, $port, $auth, $dbnum);

        // Connection
        $this->connect();
    }

    /**
     * setCredentials function.
     *
     * @access private
     * @param string $host
     * @param int $port
     * @param string $auth
     * @param int $dbnum
     * @return void
     */
    private function setCredentials(string $host, int $port, string $auth, int $dbnum)
    {
        // Set local vars
        $this->_host = $host;
        $this->_port = $port;
        $this->_auth = $auth;
        $this->_dbnum = $dbnum;
    }

    /**
     * setConnection function.
     *
     * @access private
     * @param mixed $connection (default: null)
     * @return void
     */
    private function setConnection($connection = null)
    {
        $this->_connection = $connection;
    }

    /**
     * getConnection function.
     *
     * @access public
     * @return Redis instance
     */
    public function getConnection()
    {
        return $this->_connection;
    }

    /**
     * connect function.
     *
     * @access private
     * @return bool
     */
    private function connect(): bool
    {
        // Connection
        $connection = new \Redis();
        $connection->connect($this->_host, $this->_port);

        // Auth
        if (!empty($this->_auth)) {
            $connection->auth($this->_auth);
        }

        // Db num
        if (!empty($this->_dbnum)) {
            $connection->select($this->_dbnum);
        }

        // If we have an error
        if ($connection->getLastError()) {
            return false;
        }

        // Set connection
        $this->setConnection($connection);

        return true;
    }
}
