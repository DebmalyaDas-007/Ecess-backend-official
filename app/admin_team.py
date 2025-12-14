from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from database.database import db
from schemas.team_schema import TeamMemberCreate, TeamMemberUpdate
from fastapi.security import HTTPBearer
from fastapi import UploadFile, File
from app.cloudinary_sevice import upload_image

security = HTTPBearer()

router = APIRouter(
    prefix="/admin/team",
    tags=["Admin Team Members"],
    dependencies=[Depends(security)]
)


@router.post("/add")
async def create_team_member(member: TeamMemberCreate):

    member_dict = member.dict()
    result = await db["team"].insert_one(member_dict)
    member_dict["_id"] = str(result.inserted_id)

    return {
        "message": "Team member added successfully",
        "member": member_dict
    }

@router.post("/upload-member-image/{member_id}")
async def upload_team_member_image(member_id: str, image: UploadFile = File(...)):

    if not ObjectId.is_valid(member_id):
        raise HTTPException(status_code=400, detail="Invalid member ID")

    image_url = await upload_image(image)

    await db["team"].update_one(
        {"_id": ObjectId(member_id)},
        {"$set": {"image_url": image_url}}
    )

    return {
        "message": "Image uploaded successfully",
        "image_url": image_url
    }



@router.put("/{member_id}")
async def update_team_member(member_id: str, updates: TeamMemberUpdate):

    if not ObjectId.is_valid(member_id):
        raise HTTPException(status_code=400, detail="Invalid member ID")

    update_data = {k: v for k, v in updates.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="Nothing to update")

    result = await db["team"].update_one(
        {"_id": ObjectId(member_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Member not found")

    updated = await db["team"].find_one({"_id": ObjectId(member_id)})
    updated["_id"] = str(updated["_id"])

    return {
        "message": "Member updated successfully",
        "member": updated
    }

@router.delete("/{member_id}")
async def delete_team_member(member_id: str):

    if not ObjectId.is_valid(member_id):
        raise HTTPException(status_code=400, detail="Invalid member ID")

    result = await db["team"].delete_one({"_id": ObjectId(member_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Member not found")

    return {"message": "Team member deleted successfully", "id": member_id}
