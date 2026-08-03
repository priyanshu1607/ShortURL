import json
from fastapi import Request, HTTPException
from redis_client import rateLimiter


class Rate_limiter:

    def __init__(self):
        self.rateLimiterRedisClient = rateLimiter()
        

    def Limiter(max_requests, time_frame):
        pass
