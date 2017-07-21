#!/usr/bin/env python3

from .RpqLua import RpqLua


class RpqQueue:

    def __init__(self, redis, queueName):
        """
            Registers RpqLua queue from a Redis connection
        """

        # RpqLua instance
        self.queue = RpqLua(redis)

        # Set queue name
        self.setqueueName(queueName)

    def eval(self, args):
        return self.queue.eval(*args)

    def bytesDecode(self, item):
        """
            Decode Bytes to utf-8 for Python 3 compatibility
        """

        return item.decode("utf-8")

    def setqueueName(self, queueName):
        """
            Define loaded queue name at class level
        """

        self.queueName = queueName

    def push(self, item, priority=None):
        """
            Push an item
        """

        # Build arg list
        args = ['push', self.queueName, item]
        if priority is not None:
            args.append(priority)

        return self.eval(args)

    def pop(self, orderBy='desc'):
        """
            alias for popOne()
        """

        return self.popOne(orderBy)

    def popOne(self, orderBy='desc'):
        """
            Pop an item
        """

        item = self.popMany(orderBy, 1)

        if item:  # There is an item
            return item[0]
        else:
            return None

    def popMany(self, orderBy='desc', numberOfItems=1):
        """
            Pop many items
        """

        items = self.eval(['pop', self.queueName, orderBy, numberOfItems])
        if items:
            # Decode all items from bytes to utf-8
            items = tuple(map(self.bytesDecode, items))

            return items
        else:
            return None

    def peek(self, orderBy='desc'):
        """
            alias for peekOne()
        """

        return self.peekOne(orderBy)

    def peekOne(self, orderBy='desc'):
        """
            Peek an item
        """

        item = self.peekMany(orderBy, 1)

        if item:  # There is an item
            return item[0]
        else:
            return None

    def peekMany(self, orderBy='desc', numberOfItems=1):
        """
            Peek many items
        """

        items = self.eval(['peek', self.queueName, orderBy, numberOfItems])
        if items:
            # Decode all items from bytes to utf-8
            items = tuple(map(self.bytesDecode, items))

            return items
        else:
            return None

    def count(self, priorityMin=None, priorityMax=None):
        """
            Get queue size
        """

        # Build arg list
        args = ['size', self.queueName]
        if priorityMin is not None:
            args.append(priorityMin)
            if priorityMax is not None:
                args.append(priorityMax)

        return self.eval(args)
