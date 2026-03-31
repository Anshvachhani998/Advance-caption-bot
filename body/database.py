import motor.motor_asyncio
from info import *

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB)
db = client.captions_with_chnl
chnl_ids = db.chnl_ids
users = db.users

async def addCap(chnl_id, caption):
    dets = {"chnl_id": chnl_id, "caption": caption}
    await chnl_ids.insert_one(dets)


async def updateCap(chnl_id, caption):
    await chnl_ids.update_one({"chnl_id": chnl_id}, {"$set": {"caption": caption}})

async def insert(user_id):
    user_det = {"_id": user_id}
    try:
        await users.insert_one(user_det)
    except:
        pass
        
async def total_user():
    user = await users.count_documents({})
    return user


# Get all user details
async def get_all_users():
    return await users.find({}).to_list(length=10000)

# Get all channel details
async def get_all_channels():
    return await chnl_ids.find({}).to_list(length=10000)

async def delete(id):
    await users.delete_one(id)