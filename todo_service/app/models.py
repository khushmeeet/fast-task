import datetime
from typing import List, Optional
from typing_extensions import Literal
from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.networks import EmailStr
from pydantic.types import FutureDate
from db import StatusEnum


class TodosModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    uid: EmailStr
    title: str
    desc: Optional[str]
    tags: Optional[List[str]]
    flag: Optional[bool] = False
    date: Optional[FutureDate]
    time: Optional[datetime.time]
    status: StatusEnum = StatusEnum.NDONE


class TodosModelList(BaseModel):
    todos: list[TodosModel]
