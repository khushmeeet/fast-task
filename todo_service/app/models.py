import datetime
from typing import List, Optional
from typing_extensions import Literal
from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.networks import EmailStr
from pydantic.types import FutureDate
from db import StatusEnum


class TodosModel(BaseModel):
    id: str = Field(..., alias="_id")
    title: str
    desc: Optional[str]
    tags: Optional[List[str]]
    flag: Optional[bool] = False
    date: Optional[FutureDate]
    time: Optional[datetime.time]
    status: StatusEnum = StatusEnum.NDONE


class TodosModelList(BaseModel):
    todos: list[TodosModel]
