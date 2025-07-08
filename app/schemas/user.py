from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: str

class SignUp(UserBase):
    password: str

    @field_validator("password")
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

class UserUpdate(UserBase):
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    id: str
    name: str
    email: EmailStr
    is_active: bool

class Login(BaseModel):
    email: EmailStr
    password: str
    
class Config:
    orm_mode = True
