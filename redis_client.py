import redis
import json
from constants import RedisHOST


def getRedisClient(db):
    return redis.Redis(host=RedisHOST, port=6379, db=db)
    
def setInRedis(key, value):
    getRedisClient(0).set(key, value, ex=3600)
    
def getFromRedis(key):
    redis_value = getRedisClient(0).get(key)
    if redis_value:
        redis_value = redis_value.decode("UTF-8")
    return redis_value
def rateLimiter():
    return getRedisClient(1)