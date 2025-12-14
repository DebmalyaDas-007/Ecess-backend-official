from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database.database import db
from schemas.event_schema import EventCreate,EventUpdate
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi import UploadFile, File
from app.cloudinary_sevice import upload_image

security = HTTPBearer()

router = APIRouter(
    prefix="/admin/events",
    tags=["Admin Events"],
    dependencies=[Depends(security)]  
)

@router.post("/post")
async def create_event(event: EventCreate):

    event_dict = event.dict()

    result = await db["events"].insert_one(event_dict)

    event_dict["_id"] = str(result.inserted_id)

    return {
        "message": "Event created successfully",
        "event": event_dict
    }

@router.post("/upload-image/{event_id}")
async def upload_event_image(event_id: str, image: UploadFile = File(...)):

    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid event ID")

    image_url = await upload_image(image)

    await db["events"].update_one(
        {"_id": ObjectId(event_id)},
        {"$set": {"image_url": image_url}}
    )

    return {
        "message": "Image uploaded successfully",
        "image_url": image_url
    }

@router.put("/{event_id}/update")
async def update_event(event_id: str, event: EventUpdate):

    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid event ID")

    update_data = {k: v for k, v in event.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    result = await db["events"].update_one(
        {"_id": ObjectId(event_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")

    updated_event = await db["events"].find_one({"_id": ObjectId(event_id)})
    updated_event["_id"] = str(updated_event["_id"])

    return {
        "message": "Event updated successfully",
        "event": updated_event
    }

@router.delete("/{event_id}")
async def delete_event(event_id: str):

    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid event ID")

    result = await db["events"].delete_one({"_id": ObjectId(event_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")

    return {
        "message": "Event deleted successfully",
        "event_id": event_id
    }
