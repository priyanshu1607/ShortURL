import redis
import json
from constants import RedisHOST


def getRedisClient(db):
    # print("RedisHOST", redis.Redis(host=RedisHOST, db=db))
    return redis.Redis.from_url(url=RedisHOST, db=db)

redisClient = getRedisClient(0)
def setInRedis(key, value, TTL = 1800):
    redisClient.set(key, value, ex=TTL)
    
def getFromRedis(key):
    redis_value = redisClient.get(key)
    if redis_value:
        redis_value = redis_value.decode("UTF-8")
    return redis_value
