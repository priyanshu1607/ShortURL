from motor.motor_asyncio import AsyncIOMotorClient
from constants import MongoClient

MONGO_URL = MongoClient
client = AsyncIOMotorClient(MONGO_URL)
db = client["URL"]

URL_collection = db["URL"]