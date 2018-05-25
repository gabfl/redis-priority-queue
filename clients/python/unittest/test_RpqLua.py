import unittest

import redis

from ..lib.RpqLua import RpqLua


class Test(unittest.TestCase):

    redis_host = '127.0.0.1'
    # redis_port = 8379
    redis_port = 6379
    redis_db = 0
    redis_password = ''
    lua_path = 'src/redis-priority-queue.lua'

    def setUp(self):
        # Redis instance
        self.r = redis.StrictRedis(
            host=self.redis_host, port=self.redis_port, db=self.redis_db, password=self.redis_password)

        # RpqQueue instance
        self.rl = RpqLua(self.r)

    def test_setRedisConnection(self):
        self.assertTrue(self.rl.setRedisConnection(self.r))

    def test_loadSource(self):
        self.assertTrue(self.rl.loadSource(self.lua_path))

    def test_getSha1(self):
        self.rl.loadSource('clients/python/unittest/assets/file/file.txt')

        self.assertEqual(self.rl.getSha1(),
                         '94e66df8cd09d410c62d9e0dc59d3a884e458e05')

    def test_exists(self):
        self.rl.loadSource(self.lua_path)
        self.rl.load()
        self.assertTrue(self.rl.exists())

        # Test with an invalid sha1
        self.rl.sha1 = 'non_existent_sha1'
        self.assertFalse(self.rl.exists())

    def test_load(self):
        self.rl.loadSource(self.lua_path)
        self.assertTrue(self.rl.load())

    def test_register(self):
        self.rl.loadSource(self.lua_path)
        self.assertTrue(self.rl.register())

        # Test register after flushing db
        self.r.script_flush()
        self.rl.loadSource(self.lua_path)
        self.assertTrue(self.rl.register())

    def test_eval(self):
        self.rl.loadSource(self.lua_path)
        self.rl.load()
        self.assertTrue(self.rl.eval(
            'push', 'test_rpqlua_eval', 'one') in [0, 1])
