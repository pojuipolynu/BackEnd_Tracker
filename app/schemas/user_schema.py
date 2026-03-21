from pydantic import BaseModel
from typing import List
from uuid import UUID

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID
    class Config:
        orm_mode = True
        from_attributes = True

class SignInRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str

class SignUpRequest(UserCreate):
    pass

class UserUpdateRequest(BaseModel):
    username: str | None = None
    hashed_password: str | None = None

class UserDetail(BaseModel):
    user: User


class Users(BaseModel):
    users: list[User]
