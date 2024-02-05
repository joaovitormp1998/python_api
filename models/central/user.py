from pydantic import BaseModel, constr

from typing import Optional
from datetime import datetime


class User(BaseModel):
    email: str
    name: str
    last_name: Optional[str]
    phone:Optional[str]
    photo: Optional[str]
    document: Optional[str]
    remember_token: Optional[str]
    created_at: datetime
    updated_at: datetime
    email_verified_at: datetime
    group_id: int
    
    
class UserSignUp(User):
    password: str

    
class UserSignIn(BaseModel):
    email: str
    password: str
    
class UserToken(BaseModel):
    id: int
    email: str
    name: str
    group_id: int
    token: Optional[str] = None


class Address(BaseModel):
    zip_code: Optional[str]
    city:Optional[str]
    country: constr(max_length = 2)
    state: constr(max_length = 2)
    address_line: Optional[str]
    address_line_2: Optional[str]


class UserProfile(BaseModel):
    name: str
    last_name: Optional[str] = None
    email: str
    photo: Optional[str] = None
    phone: Optional[str] = None
    document: Optional[str] = None
    group_id: int
    address: Optional[Address] = None
