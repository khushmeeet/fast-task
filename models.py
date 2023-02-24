import datetime
from typing import List, Optional
from typing_extensions import Literal
from pydantic import BaseModel
from pydantic.networks import EmailStr
from pydantic.types import FutureDate


class TodosModel(BaseModel):
    id: int
    title: str
    desc: Optional[str]
    tags: Optional[List[str]]
    flag: Optional[bool]
    date: Optional[FutureDate]
    time: Optional[datetime.time]
    status: Literal["done", "ndone", "archived"]


class TodosModelList(BaseModel):
    todos: list[TodosModel]


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
