from typing import Optional
from pydantic import BaseModel
from pydantic.networks import EmailStr


class TokenModel(BaseModel):
    token: str


class VerifyTokenResponseModel(BaseModel):
    detail: str
    condition: bool
    email: Optional[EmailStr]
