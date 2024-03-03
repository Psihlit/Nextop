from typing import Optional

from pydantic import BaseModel, Field


class OrderSchema(BaseModel):
    id: int
    status_id: int
    start_address: str
    end_address: str
    cost: float
    user_id: int
    dispatcher_id: int
    driver_id: int

    class Config:
        orm_mode = True


class OrderCreate(BaseModel):
    status_id: Optional[int] = Field(gt=0, default=1)
    start_address: Optional[str] = Field(default="new start address")
    end_address: Optional[str] = Field(default="new end address")
    cost: float = Field(gt=0, default=1000)
    user_id: Optional[int] = Field(gt=0, default=1)
    dispatcher_id: Optional[int] = Field(gt=0, default=1)
    driver_id: Optional[int] = Field(gt=0, default=1)


class OrderUpdate(BaseModel):
    status_id: Optional[int] = Field(gt=0, default=1)
    start_address: Optional[str] = Field(default="new start address")
    end_address: Optional[str] = Field(default="new end address")
    cost: float = Field(gt=0, default=1000)
    user_id: Optional[int] = Field(gt=0, default=1)
    dispatcher_id: Optional[int] = Field(gt=0, default=1)
    driver_id: Optional[int] = Field(gt=0, default=1)


class ResponseModel(BaseModel):
    status: str
    status_code: str
    data: list[OrderSchema]
    details: Optional[str] = None
