from typing import List, Optional
from typing_extensions import Literal
from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.networks import EmailStr


class UserModel(BaseModel):
    first_name: str
    last_name: Optional[str]
    email: EmailStr
    # TODO: Support for password hash
    pass_hash: str
    # disabled: bool


class JWTModel(BaseModel):
    access_token: str
    token_type: str
