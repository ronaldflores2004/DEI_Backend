from pydantic import BaseModel, EmailStr

from app.shared.enums.role_enum import RoleEnum


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum