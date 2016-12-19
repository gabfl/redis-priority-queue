#!/usr/bin/env python3

class RpqQueue:
    queue = None # Loaded queue
    queueName = None # Queue name

    # Check if there are elements in an iterable variable
    def has_elements(self, item):
        try:
            i = iter(item)
            next(i)

            return True
        except StopIteration:
            return False

    # Define loaded LUA at class level
    def setLuaScript(self, luaScript):
        self.queue = luaScript;

    # Define loaded queue name at class level
    def setqueueName(self, queueName):
        self.queueName = queueName;

    # Push an item
    def push(self, item, priority = None):
        # Build arg list
        args = ['push', self.queueName, item]
        if (priority != None):
            args.append(priority);

        return self.queue(args = args)

    # alias for popOne()
    def pop(self, orderBy = 'desc'):
        return self.popOne(orderBy)

    # Pop an item
    def popOne(self, orderBy = 'desc'):
        item = self.popMany(orderBy, 1)

        if self.has_elements(item): # There is an item
            return item[0];
        else:
            return None;

    # Pop many items
    def popMany(self, orderBy = 'desc', numberOfItems = 1):
        return self.queue(args = ['pop', self.queueName, orderBy, numberOfItems])

    # Peek in a queue
    def peek(self, orderBy = 'desc', numberOfItems = 1):
        return self.queue(args = ['peek', self.queueName, orderBy, numberOfItems])

    # Get queue size
    def count(self, priorityMin = None, priorityMax = None):
        # Build arg list
        args = ['size', self.queueName]
        if (priorityMin != None):
            args.append(priorityMin);
        if (priorityMin != None and priorityMax != None):
            args.append(priorityMax);

        return self.queue(args = args)
