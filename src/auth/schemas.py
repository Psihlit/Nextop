from typing import Optional

from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[int]):
    id: int
    name: str
    surname: str
    email: str
    phone_number: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    name: Optional[str] = Field(default="name")
    surname: Optional[str] = Field(default="surname")
    email: Optional[str] = Field(pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                                 default="test@mail.com")
    password: Optional[str] = Field(min_length=5, default="12345")
    phone_number: Optional[str] = Field(pattern=r'\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}',
                                        default="+7 (XXX) XXX-XX-XX",
                                        description="Phone number must be in the format +7 (XXX) XXX-XX-XX")
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
