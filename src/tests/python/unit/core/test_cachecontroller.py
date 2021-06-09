import unittest


class TestCacheController(unittest.TestCase):
    def test_connection(self):
        """
            Test redis connection
        """
        from core.controller.cachecontroller import CacheController
        sid_cache = CacheController(
            user_id='admin'
        )
        sid_cache.setup()
        self.assertIsNotNone(sid_cache.redis_conn)

    def test_key(self):
        """
            Test redis dict
        """
        from core.controller.cachecontroller import CacheController
        sid_cache = CacheController(
            user_id='admin'
        )
        sid_cache.setup()
        sid_cache.set_key('test', 'mykey', 'myvalue')

        self.assertEqual(sid_cache.get_key('test', 'mykey'), 'myvalue')
