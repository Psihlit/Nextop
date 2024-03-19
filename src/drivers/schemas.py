from typing import Optional

from pydantic import BaseModel, Field


class DriverSchema(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    phone_number: str
    dispatcher_id: int


class ResponseModel(BaseModel):
    status: str
    status_code: str
    data: list[DriverSchema]
    details: Optional[str] = None


class DriverCreate(BaseModel):
    name: Optional[str] = Field(default="testname")
    surname: Optional[str] = Field(default="testsurname")
    email: Optional[str] = Field(pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                                 default="test@mail.com")
    password: Optional[str] = Field(min_length=5, default="12345")
    phone_number: Optional[str] = Field(pattern=r'\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}',
                                        default="+7 (XXX) XXX-XX-XX",
                                        description="Phone number must be in the format +7 (XXX) XXX-XX-XX")
    dispatcher_id: Optional[int] = Field(gt=0, default=1)


class DriverUpdate(BaseModel):
    name: Optional[str] = Field(default="testname")
    surname: Optional[str] = Field(default="testsurname")
    email: Optional[str] = Field(pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                                 default="test@mail.com")
    password: Optional[str] = Field(min_length=5, default="12345")
    phone_number: Optional[str] = Field(pattern=r'\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}',
                                        default="+7 (XXX) XXX-XX-XX",
                                        description="Phone number must be in the format +7 (XXX) XXX-XX-XX")
    dispatcher_id: Optional[int] = Field(gt=0, default=1)
