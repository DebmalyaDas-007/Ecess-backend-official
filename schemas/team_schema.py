from pydantic import BaseModel
from typing import Optional

class TeamMemberCreate(BaseModel):
    name: str
    post: str
    year: str
    LinkedInHandle: Optional[str] = None
    InstaHandle: Optional[str] = None
    image_url: Optional[str] = None


class TeamMemberUpdate(BaseModel):
    name: Optional[str] = None
    post: Optional[str] = None
    year: Optional[str] = None
    LinkedInHandle: Optional[str] = None
    InstaHandle: Optional[str] = None
    image_url: Optional[str] = None
