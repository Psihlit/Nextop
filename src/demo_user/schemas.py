from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    email: EmailStr
    surname: str
    name: str
    phone_number: str
    is_active: bool
    is_superuser: bool
    is_verified: bool


class ResponseUserSchema(UserSchema):
    id: int


class ResponseModel(BaseModel):
    status: str
    status_code: str
    data: list[ResponseUserSchema]
    details: Optional[str] = None


class UserCreate(UserSchema):
    surname: Optional[str] = Field(default="surname")
    name: Optional[str] = Field(default="name")
    hashed_password: Optional[str] = Field(min_length=5, default="12345")
    phone_number: Optional[str] = Field(pattern=r'\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}',
                                        default="+7 (XXX) XXX-XX-XX",
                                        description="Phone number must be in the format +7 (XXX) XXX-XX-XX")
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


# UserAuth = UserCreate

class UserAuth(BaseModel):
    email: EmailStr
    hashed_password: Optional[str] = Field(min_length=5, default="12345")
