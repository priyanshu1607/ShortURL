import os

HOST  =  'localhost'
RedisHOST = os.getenv("REDIS_URL")
MongoClient = os.getenv("MONGO_URL")
secreat_key = os.getenv("Secret_Key")