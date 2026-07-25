from pydantic import BaseModel, EmailStr, Field

from app.shared.enums.role_enum import RoleEnum


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: RoleEnum