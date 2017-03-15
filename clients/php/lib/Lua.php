<?php
namespace RedisPriorityQueue;

class Lua
{
    // Private
    private $_connection; // Redis instance
    private $_luaFilePath; // Path of Lua script
    private $_sha; // Loaded sha into Redis
    private $_args = []; // Array of arguments

    /**
     * __construct function.
     *
     * @access public
     * @param mixed $connection
     * @return void
     */
    public function __construct($connection)
    {
        // Set Redis connection
        $this->setConnection($connection);
    }

    /**
     * setConnection function.
     *
     * @access protected
     * @param mixed $connection (default: null)
     * @return void
     */
    protected function setConnection($connection = null)
    {
        $this->_connection = $connection;
    }

    /**
     * setpath function.
     *
     * @access protected
     * @param mixed $path
     * @return bool
     */
    protected function setpath($path): bool
    {
        if (file_exists($path)) {
            $this->_luaFilePath = $path;
            return true;
        }

        return false;
    }

    /**
     * setArgs function.
     *
     * @access public
     * @param array $args
     * @return bool
     */
    public function setArgs(array $args): bool
    {
        $this->_args = $args;

        return true;
    }

    /**
     * setSha function.
     *
     * @access private
     * @param string $sha
     * @return void
     */
    private function setSha(string $sha)
    {
        $this->_sha = $sha;
    }

    /**
     * loadScript function.
     *
     * @access private
     * @return bool
     */
    private function loadScript(): bool
    {
        // Return true if we have already the script
        if ($this->_sha) {
            return true;
        }

        // If the file exists
        if (file_exists($this->_luaFilePath)) {
            // Get the sha1 of the LUA file
            $fileSha = $this->getLuaFileSha();

            // Check if the script is already loaded in Redis
            if ($this->exists($fileSha)) {
                // Set script hash
                $this->setSha($fileSha);

                return true;
            }

            // Get script content
            $script = file_get_contents($this->_luaFilePath);

            // Load into Redis
            $sha = $this->_connection->script("load", $script);
            $this->setSha($sha);

            return true;
        }

        return false;
    }

    /**
     * Get the sha1 of the LUA file
     * @return string
     */
    private function getLuaFileSha(): string
    {
        return sha1_file($this->_luaFilePath);
    }

    /**
     * Check if the script is already loaded in Redis
     * @param  string $sha Sha of LUA script
     * @return bool
     */
    private function exists(string $sha): bool
    {
        // Check if the script exists in Redis
        $exists = $this->_connection->script('exists', $sha);

        return (isset($exists[0]) && $exists[0] == 1) ? true : false;
    }

    /**
     * run function.
     *
     * @access protected
     * @return evalsha result
     */
    protected function run()
    {
        // Load script
        if (!$this->loadScript()) {
            return 0;
        }

        return $this->_connection->evalSha($this->_sha, $this->_args);
    }
}
