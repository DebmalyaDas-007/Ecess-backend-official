from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URI
import asyncio
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
client= AsyncIOMotorClient(MONGODB_URI)
db= client["ecessdb"]

async def check_mongo_connection():
    try:
        await client.admin.command('ping')
        logging.info("SUCCESS: MongoDB connection established to 'ecessdb'!")
        return True
    except Exception as e:
        logging.error(f"ERROR: MongoDB connection failed. Details: {e}")
        return False