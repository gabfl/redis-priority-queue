#!/usr/bin/env python3

class RpqLua:
    def __init__(self, redisConnection):
        '''Sets Redis connection, load LUA from path'''

        self.setRedisConnection(redisConnection);
        self.loadSource(self.getLuaPath());

    def getLuaPath(self):
        """
            Returns the LUA path in the filesystem
        """

        import rpq_src, pkg_resources

        return pkg_resources.resource_filename('rpq_src', 'redis-priority-queue.lua');

    def file_get_contents(self, filename):
        '''Get a file content'''

        with open(filename) as f:
            return f.read()

    def setRedisConnection(self, connection):
        '''Set a Redis connection'''

        self.connection = connection;

    def loadSource(self, path):
        '''Load LUA script source code from a file'''

        self.source = self.file_get_contents(path);

    def register(self):
        '''Load the script into Redis'''

        self.queue = self.connection.register_script(self.source)
        return self.queue;
