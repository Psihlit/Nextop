from typing import Optional

from pydantic import BaseModel, Field


class OrderTypeSchema(BaseModel):
    id: int
    status: str


class ResponseModel(BaseModel):
    status: str
    status_code: str
    data: list[OrderTypeSchema]
    details: Optional[str] = None


class OrderTypeCreate(BaseModel):
    status: Optional[str] = Field(default="new status")


class OrderTypeUpdate(BaseModel):
    status: Optional[str] = Field(default="new status")
