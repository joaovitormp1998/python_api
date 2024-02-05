from pydantic import BaseModel

from typing import Optional, List
from datetime import datetime


class LinktreeLinksCreate(BaseModel):
    text: str
    url: str
    

class LinktreeCreate(BaseModel):
    name: str
    colorBackLink: str
    colorBackground: str
    colorName: str
    colorNameLink: str
    image: str
    links: List[LinktreeLinksCreate] = []


class LinktreeLinksResponse(BaseModel):
    id: int
    linktree_id: int
    social_name: str
    social_link: str


class LinktreeResponse(BaseModel):
    id: int
    user_id: int
    url: str
    name: str
    colorBackLink: str
    colorBackground: str
    colorName: str
    colorNameLink: str
    image: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    links: List[LinktreeLinksResponse] = []

