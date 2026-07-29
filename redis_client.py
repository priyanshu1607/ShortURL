import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def setInRedis(key, value):
    redis_client.set(key, value, ex=3600)
    
def getFromRedis(key):
    redis_value = redis_client.get(key)
    if redis_value:
        redis_value = redis_client.get(key)
    return redis_value
    