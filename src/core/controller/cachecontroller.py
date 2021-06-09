"""
  Description:    Cache Controller
"""
import logging
import redis

from core.general import settings
from core.general.exceptions import SIDException
from core.decorator.singleton import Singleton


class CacheController(metaclass=Singleton):
    """
        Cache Controller
    """

    def __init__(self, *args, **kwargs):
        self.hostname = 'sid_redis'
        self.redis_conn = None

        allowed_fields = set(['user_id'])
        for field in allowed_fields:
            try:
                setattr(self, field, kwargs[field].strip())
            except Exception:
                setattr(self, field, None)

    def setup(self):
        """
            setuo connection
        """
        self.redis_conn = redis.Redis(self.hostname, decode_responses=True)
        try:
            self.redis_conn.ping()
        except Exception as exp:
            logging.error(str(exp))
            raise SIDException('Redis Connection Error')

    def set_key(self, dict_name, key, value):
        """
            set key
        """
        return self.redis_conn.hset(dict_name, key, value)

    def set_dict(self, dict_name, dictlist):
        """
            we do the bulk hset using pipeline
        """
        if not dictlist:
            return

        pipeline = self.redis_conn.pipeline()

        for key, value in dictlist.items():
            if key:
                pipeline.hset(dict_name, key, value)

        pipeline.execute()

    def get_key(self, dict_name, key):
        """
            get key
        """
        return self.redis_conn.hget(dict_name, key)

    def key_exists(self, dict_name):
        """
            check if dict exists
        """
        return self.redis_conn.exists(dict_name) > 0

    def cleanup(self):
        """
            remove all the keys
        """
        if self.redis_conn:
            keys = self.redis_conn.keys('*')
            for key in keys:
                self.redis_conn.delete(key)

    # def __del__(self):
    #     self.cleanup()
