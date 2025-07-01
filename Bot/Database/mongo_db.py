from motor.motor_asyncio import AsyncIOMotorClient
from Bot.config import MongoConf

mongo = AsyncIOMotorClient(MongoConf.MONGO_URL)
DB = mongo[MongoConf.MONGO_DB_NAME]


async def save_user_data(
    user_id: int,
    telegram_name: str,
    leetcode_username: str = None,
    striver_username: str = None,
) -> None:
    """
    Save user data to the MongoDB database.
    """

    doc = {"name": telegram_name}
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


async def delete_user_data(user_id: int, action: str) -> bool:
    """
    Delete user data from the MongoDB database.
    Actions: 'leetcode', 'striver'
    """
    collection = DB["users"]

    data = await collection.find_one({"_id": user_id})
    if not data:
        return False

    field_map = {"leetcode": "leetcode_username", "striver": "striver_username"}
    other_field_map = {"leetcode": "striver_username", "striver": "leetcode_username"}

    field_to_remove = field_map.get(action)
    if not field_to_remove:
        return False

    # If the other field doesn't exist, delete the entire document
    if not data.get(other_field_map[action]):
        result = await collection.delete_one({"_id": user_id})
        return result.deleted_count > 0

    # Otherwise, just remove the specified field
    await collection.update_one({"_id": user_id}, {"$unset": {field_to_remove: ""}})
    return True
