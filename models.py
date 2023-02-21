import datetime
from typing import List
from typing_extensions import Literal
from pydantic import BaseModel
from pydantic.networks import NameEmail
from pydantic.types import FutureDate


class Todos(BaseModel):
    title: str
    desc: str
    tags: List[str]
    flag: bool
    date: FutureDate
    time: datetime.time
    status: Literal["done", "ndone", "archived"]


class User(BaseModel):
    first_name: str
    last_name: str
    email: NameEmail
    # TODO: Support for password hash
    pass_hash: str
