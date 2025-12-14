from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Any
from datetime import datetime
from bson import ObjectId 

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class MongoBase(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat(),
        }
    }


class TeamMembers(MongoBase):
    name:str
    post:str
    year:str
    LinkedInHandle:Optional[str]
    InstaHandle:Optional[str]
    image_url: Optional[str] = None


class Event(MongoBase):
    name:str
    shortDesc:str
    longDesc:str
    date:datetime
    time:str
    venue:str
    is_published: bool = False
    image_url:Optional[str]=None




