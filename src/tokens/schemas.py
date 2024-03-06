from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    user_id: int


class ResponseModel(BaseModel):
    status: str
    status_code: str
    data: Token
    details: Optional[str] = None
