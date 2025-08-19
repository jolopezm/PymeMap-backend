from fastapi import APIRouter
from app.db import db
from app.models import User

router = APIRouter()

@router.get("/users")
async def get_users():
    users = []
    cursor = db.users.find({})
    async for document in cursor:
        document["_id"] = str(document["_id"])
        users.append(document)
    return users

@router.post("/user")
async def create_user(user: User):
    result = await db.users.insert_one(user.dict())
    return {"inserted_id": str(result.inserted_id)}
