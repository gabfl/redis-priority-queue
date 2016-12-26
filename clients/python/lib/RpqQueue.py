#!/usr/bin/env python3

class RpqQueue:
    queue = None # Loaded queue
    queueName = None # Queue name

    def bytesDecode(self, item):
        '''Decode Bytes to utf-8 for Python 3 compatibility'''
        return item.decode("utf-8");

    def setLuaScript(self, luaScript):
        '''Define loaded LUA at class level'''
        self.queue = luaScript;

    def setqueueName(self, queueName):
        '''Define loaded queue name at class level'''
        self.queueName = queueName;

    def push(self, item, priority = None):
        '''Push an item'''
        # Build arg list
        args = ['push', self.queueName, item]
        if (priority != None):
            args.append(priority);

        return self.queue(args = args)

    def pop(self, orderBy = 'desc'):
        '''alias for popOne()'''
        return self.popOne(orderBy)

    def popOne(self, orderBy = 'desc'):
        '''Pop an item'''
        item = self.popMany(orderBy, 1)

        if item: # There is an item
            return item[0];
        else:
            return None;

    def popMany(self, orderBy = 'desc', numberOfItems = 1):
        '''Pop many items'''
        items = self.queue(args = ['pop', self.queueName, orderBy, numberOfItems])
        if items:
            # Decode all items from bytes to utf-8
            items = tuple(map(self.bytesDecode, items));

            return items;
        else:
            return None;

    def peek(self, orderBy = 'desc'):
        '''alias for peekOne()'''
        return self.peekOne(orderBy)

    def peekOne(self, orderBy = 'desc'):
        '''Peek an item'''
        item = self.peekMany(orderBy, 1)

        if item: # There is an item
            return item[0];
        else:
            return None;

    def peekMany(self, orderBy = 'desc', numberOfItems = 1):
        '''Peek many items'''
        items = self.queue(args = ['peek', self.queueName, orderBy, numberOfItems])
        if items:
            # Decode all items from bytes to utf-8
            items = tuple(map(self.bytesDecode, items));

            return items;
        else:
            return None;

    def count(self, priorityMin = None, priorityMax = None):
        '''Get queue size'''
        # Build arg list
        args = ['size', self.queueName]
        if (priorityMin != None):
            args.append(priorityMin);
        if (priorityMin != None and priorityMax != None):
            args.append(priorityMax);

        return self.queue(args = args)
