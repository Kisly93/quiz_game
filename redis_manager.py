import redis
import os
from dotenv import load_dotenv

load_dotenv()


class RedisManager:
    def __init__(self):
        REDIS_HOST = os.getenv('REDIS_HOST')
        REDIS_PORT = os.getenv('REDIS_PORT')
        REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
        self.redis_db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)

    def get_redis_db(self):
        return self.redis_db
