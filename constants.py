import os

HOST  =  'localhost:8000'
RedisHOST = os.getenv("REDIS_URL")
MongoClient = os.getenv("MONGO_URL")