import unittest

import redis
import prettytable
from prettytable import PrettyTable

from .. import queue_monitor


class Test(unittest.TestCase):

    redis_host = '127.0.0.1'
    # redis_port = 8379
    redis_port = 6379
    redis_db = 0
    redis_password = ''

    def setUp(self):
        # Redis instance
        self.r = redis.StrictRedis(
            host=self.redis_host, port=self.redis_port, db=self.redis_db, password=self.redis_password)

    def test_setSortGroups(self):
        self.assertIsInstance(queue_monitor.setSortGroups(), list)
        self.assertIsInstance(queue_monitor.setSortGroups(
            [[0, 1000], [1001, 2000], [2001, 3000]]), list)

    def test_getCount(self):
        queue_monitor.r = self.r
        self.assertIsInstance(queue_monitor.getCount('some_queue'), int)

    def test_getColumnTitle(self):
        queue_monitor.r = self.r
        self.assertIsInstance(queue_monitor.getColumnTitle(), str)
        self.assertEqual(queue_monitor.getColumnTitle(), 'Total')
        self.assertEqual(queue_monitor.getColumnTitle(0, '+inf'), 'From 0')
        self.assertEqual(queue_monitor.getColumnTitle(
            '-inf', 100), 'Up to 100')
        self.assertEqual(queue_monitor.getColumnTitle(
            10, 100), '10 to 100')
        self.assertEqual(queue_monitor.getColumnTitle(
            30, 30), '30')

    def test_setColumnAlign(self):
        titles = ['Queue name', 'Total', 'Up to 100', 'From 101']
        queue_monitor.t = PrettyTable(titles)
        queue_monitor.setColumnAlign(titles)
        self.assertIsInstance(queue_monitor.t, prettytable.PrettyTable)

    def test_monitor(self):
        # Table
        self.assertIsNone(queue_monitor.monitor(host=self.redis_host,
                                                port=self.redis_port,
                                                dbnum=self.redis_db,
                                                password=self.redis_password))

        # CSV
        self.assertIsNone(queue_monitor.monitor(host=self.redis_host,
                                                port=self.redis_port,
                                                dbnum=self.redis_db,
                                                password=self.redis_password,
                                                out='csv'))

    def test_monitor_2(self):
        # Test exception for invalid Redis connection
        self.assertRaises(SystemExit, queue_monitor.monitor,
                          host=self.redis_host,
                          port=1234,
                          dbnum=self.redis_db,
                          password=self.redis_password)

    def test_monitor_2(self):
        # Test exception for invalid Redis connection
        self.assertRaises(SystemExit, queue_monitor.monitor,
                          host='',
                          port=1234,
                          dbnum=self.redis_db,
                          password=self.redis_password)
