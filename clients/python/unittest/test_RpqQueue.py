import unittest

import redis

from ..lib.RpqQueue import RpqQueue


class Test(unittest.TestCase):

    def setUp(self):
        # Redis instance
        #r = redis.StrictRedis(host='127.0.0.1', port=8379, db=0, password='')
        r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password='')

        # RpqQueue instance
        self.rq = RpqQueue(r, 'test_queue')

    def test_eval(self):
        self.assertTrue(self.rq.eval(['push', 'test_queue', 'one']) in [0, 1])

    def test_bytesDecode(self):
        b = b'\xe8\xaf\xbb\xe5\x86\x99\xe6\xb1\x89\xe5\xad\x97 - \xe5\xad\xa6\xe4\xb8\xad\xe6\x96\x87'

        self.assertEqual(self.rq.bytesDecode(b), '读写汉字 - 学中文')

    def test_setqueueName(self):
        self.rq.setqueueName('some_queue')

        self.assertEqual(self.rq.queueName, 'some_queue')

    def test_push(self):
        self.assertEqual(self.rq.push('item'), 0)

    def test_pop(self):
        self.rq.setqueueName('test_pop')
        self.rq.push('my_item')
        self.assertEqual(self.rq.pop(), 'my_item')

        self.rq.setqueueName('test_pop_empty')
        self.assertIsNone(self.rq.pop())

    def test_popOne(self):
        self.rq.setqueueName('test_popOne')
        self.rq.push('my_item')
        self.assertEqual(self.rq.popOne(), 'my_item')

        self.rq.setqueueName('test_popOne_empty')
        self.assertIsNone(self.rq.popOne())

    def test_popMany(self):
        self.rq.setqueueName('test_popMany')
        self.rq.push('my_item')
        self.rq.push('my_item_2')
        self.rq.push('my_item_3')
        self.assertEqual(self.rq.popMany('desc', 3),
                         ('my_item_3', 'my_item_2', 'my_item'))

        self.rq.push('my_item')
        self.rq.push('my_item_2')
        self.rq.push('my_item_3')
        self.assertEqual(self.rq.popMany('asc', 3),
                         ('my_item', 'my_item_2', 'my_item_3'))

        self.rq.setqueueName('test_popMany_empty')
        self.assertIsNone(self.rq.popMany())

    def test_peek(self):
        self.rq.setqueueName('test_peek')
        self.rq.push('my_item')
        self.assertEqual(self.rq.peek(), 'my_item')

        self.rq.setqueueName('test_peek_empty')
        self.assertIsNone(self.rq.peek())

    def test_peekOne(self):
        self.rq.setqueueName('test_peekOne')
        self.rq.push('my_item')
        self.assertEqual(self.rq.peekOne(), 'my_item')

        self.rq.setqueueName('test_peekOne_empty')
        self.assertIsNone(self.rq.peekOne())

    def test_peekMany(self):
        self.rq.setqueueName('test_peekMany')
        self.rq.push('my_item')
        self.rq.push('my_item_2')
        self.rq.push('my_item_3')
        self.assertEqual(self.rq.peekMany('desc', 3),
                         ('my_item_3', 'my_item_2', 'my_item'))

        self.rq.push('my_item')
        self.rq.push('my_item_2')
        self.rq.push('my_item_3')
        self.assertEqual(self.rq.peekMany('asc', 3),
                         ('my_item', 'my_item_2', 'my_item_3'))

        self.rq.setqueueName('test_peekMany_empty')
        self.assertIsNone(self.rq.peekMany())

    def test_count(self):
        self.rq.setqueueName('test_count')
        self.rq.push('my_item', 10)
        self.rq.push('my_item_2', 20)
        self.rq.push('my_item_3', 30)

        self.assertEqual(self.rq.count(), 3)
        self.assertEqual(self.rq.count(priorityMin=15), 2)
        self.assertEqual(self.rq.count(priorityMin=0, priorityMax=25), 2)

        # Empty the queue
        self.rq.popMany(numberOfItems=10)
