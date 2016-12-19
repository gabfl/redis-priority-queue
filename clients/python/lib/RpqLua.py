#!/usr/bin/env python3

class RpqLua:
    connection = None # Redis Instance
    queue = None # Loaded queue
    script = None # Script source

    # Get a file content
    def file_get_contents(self, filename):
        with open(filename) as f:
            return f.read()

    # Set a Redis connection
    def setRedisConnection(self, connection):
        self.connection = connection;

    # Load LUA script source code from a file
    def loadSource(self, path):
        self.source = self.file_get_contents(path);

    # Load the script into Redis
    def register(self):
        self.queue = self.connection.register_script(self.source)
        return self.queue;

#     # Return loaded queue
#     def getQueue:
#         return self.queue;
