from fastapi import Request ,HTTPException
from redis_client import rateLimiter


class Rate_limiter:
    def __init__(self, bucket, max_requests, time_frame):
        self.bucket = bucket
        self.max_requests = max_requests
        self.time_frame = time_frame
        
    
    def __call__(self, request:Request):
        self.ip = request.client.host
        self.redisClient = rateLimiter()
        self.Limiter()
        

    def Limiter(self):
        key = f'rate_limit:{self.ip}_{self.bucket}'
        IPInRedis = self.redisClient.get(key)
        if not IPInRedis:
            self.redisClient.set(key, 1, ex = self.time_frame) 
            return
        
        IPInRedis = int(IPInRedis.decode("UTF-8"))
        if IPInRedis >= self.max_requests:
            raise HTTPException(status_code=429 , detail= "Rate excedded")
        else:
            self.redisClient.incr(key)
            
        
            
