from pydantic import BaseModel


class RegisterParameters(BaseModel):
    email: str
    password: str
    name: str


class LoginParameters(BaseModel):
    email: str
    password: str



class User(BaseModel):
    id: int
    email: str
    name: str
    group_id: int


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user: User
    expires_in: int = 1030
