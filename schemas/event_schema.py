from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EventCreate(BaseModel):
    name: str
    shortDesc: str
    longDesc: str
    date: datetime
    time: str
    venue: str
    is_published: bool = False
    image_url: Optional[str] = None


class EventUpdate(BaseModel):
    name: Optional[str] = None
    shortDesc: Optional[str] = None
    longDesc: Optional[str] = None
    date: Optional[datetime] = None
    time: Optional[str] = None
    venue: Optional[str] = None
    is_published: Optional[bool] = None
    registration_link: Optional[str] = None
    image_url: Optional[str] = None
