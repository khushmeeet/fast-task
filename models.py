import datetime
from typing import List, Optional
from typing_extensions import Literal
from pydantic import BaseModel
from pydantic.networks import EmailStr
from pydantic.types import FutureDate


class TodosModel(BaseModel):
    title: str
    desc: str
    tags: List[str]
    flag: bool
    date: FutureDate
    time: datetime.time
    status: Literal["done", "ndone", "archived"]


class UserModel(BaseModel):
    first_name: str
    last_name: Optional[str]
    email: EmailStr
    # TODO: Support for password hash
    pass_hash: str
    # disabled: bool
