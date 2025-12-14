from fastapi import APIRouter
from database.database import db
from bson import ObjectId
from fastapi import HTTPException

router = APIRouter(prefix="/team", tags=["Team"])

@router.get("")
async def get_all_team_members():
    members = []
    async for member in db["team"].find():
        member["_id"] = str(member["_id"])
        members.append(member)

    return members


@router.get("/{member_id}")
async def get_team_member(member_id: str):

    if not ObjectId.is_valid(member_id):
        raise HTTPException(status_code=400, detail="Invalid member ID")

    member = await db["team"].find_one({"_id": ObjectId(member_id)})
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    member["_id"] = str(member["_id"])
    return member
