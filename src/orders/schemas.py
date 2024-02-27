from typing import Optional

from pydantic import BaseModel, Field


class OrderSchema(BaseModel):
    id: int
    status_id: int
    start_address: str
    end_address: str
    cost: float
    user_id: int

    class Config:
        orm_mode = True


class OrderCreate(BaseModel):
    id: int
    status_id: int
    start_address: str
    end_address: str
    cost: float = Field(gt=0)
    user_id: int


class OrderUpdate(BaseModel):
    status_id: int
    start_address: str
    end_address: str
    cost: float = Field(gt=0)
    user_id: int


class ResponseModel(BaseModel):
    status: str
    status_code: str
    data: list[OrderSchema]
    details: Optional[str] = None
