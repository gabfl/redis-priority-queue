#!/usr/bin/env python3

import hashlib


class RpqLua:
    def __init__(self, redisConnection):
        '''Sets Redis connection, load LUA from path'''

        # Set Redis connection
        self.setRedisConnection(redisConnection)

        # Load LUA source
        self.loadSource(self.getLuaPath())

        # Register LUA script
        self.register()

    def getLuaPath(self):
        """
            Returns the LUA path in the filesystem
        """

        import rpq_src
        import pkg_resources

        return pkg_resources.resource_filename('rpq_src', 'redis-priority-queue.lua')

    def file_get_contents(self, filename):
        """
            Get a file content
        """

        with open(filename) as f:
            return f.read()

    def setRedisConnection(self, connection):
        """
            Set a Redis connection
        """

        self.connection = connection

        return True

    def loadSource(self, path):
        """
            Load LUA script source code from a file
        """

        self.source = self.file_get_contents(path)

        return True

    def getSha1(self):
        """
            Calculate sha1 of the LUA source
        """

        d = hashlib.sha1(self.source.encode('utf-8'))
        d.digest()
        return d.hexdigest()

    def exists(self):
        """
            Returns `True` if the LUA script is already loaded into Redis
        """

        # Check if the script exists
        t = self.connection.script_exists(self.sha1)

        if t and t[0]:
            return True

        return False

    def load(self):
        """
            Load the script into Redis
        """

        self.connection.script_load(self.source)

        return True

    def register(self):
        """
            Registers the script
        """

        # Set LUA sha1
        self.sha1 = self.getSha1()

        # Load if needed
        if not self.exists():
            self.load()

        return True

    def eval(self, *args):
        """
            Call the LUA script with the desired arguments and returns the output
        """

        return self.connection.evalsha(self.sha1, 0, *args)
