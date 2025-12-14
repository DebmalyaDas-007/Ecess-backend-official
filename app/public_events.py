from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database.database import db

router = APIRouter(
    prefix="/events",
    tags=["Public Events"]
)

@router.get("")
async def get_all_events():
    events = []
    async for event in db["events"].find():
        event["_id"] = str(event["_id"])
        events.append(event)

    return events


@router.get("/published")
async def get_published_events():
    events = []
    async for event in db["events"].find({"is_published": True}):
        event["_id"] = str(event["_id"])
        events.append(event)

    return events


@router.get("/{event_id}")
async def get_event_by_id(event_id: str):

    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid event ID")

    event = await db["events"].find_one({"_id": ObjectId(event_id)})

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event["_id"] = str(event["_id"])
    return event
