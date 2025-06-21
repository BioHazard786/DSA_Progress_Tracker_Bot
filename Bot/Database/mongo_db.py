from motor.motor_asyncio import AsyncIOMotorClient
from Bot.config import MongoConf

mongo = AsyncIOMotorClient(MongoConf.MONGO_URL)
DB = mongo[MongoConf.MONGO_DB_NAME]


async def save_user_data(
    user_id: int, leetcode_username: str = None, striver_username: str = None
) -> None:
    """
    Save user data to the MongoDB database.
    """

    doc = {}
    if leetcode_username:
        doc["leetcode_username"] = leetcode_username
    if striver_username:
        doc["striver_username"] = striver_username

    collection = DB["users"]
    await collection.update_one({"_id": user_id}, {"$set": doc}, upsert=True)


async def get_user_data(user_id: int) -> dict:
    """
    Get user data from the MongoDB database.
    """

    collection = DB["users"]
    data = await collection.find_one({"_id": user_id})
    return data or {}
