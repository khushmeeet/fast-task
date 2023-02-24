from enum import Enum
from mongoengine import (
    Document,
    StringField,
    ListField,
    BooleanField,
    DateTimeField,
    EnumField,
    EmailField,
)


class StatusEnum(Enum):
    DONE = "done"
    NDONE = "ndone"
    ARCHIVED = "archived"


class Todos(Document):
    title = StringField(required=True)
    desc = StringField()
    tags = ListField(StringField(max_length=20))
    flag = BooleanField()
    date = DateTimeField()
    time = DateTimeField()
    status = EnumField(StatusEnum, default=StatusEnum.NDONE)
    meta = {"db_alias": "todo", "collection": "Todos"}
<<<<<<< HEAD:db.py


class User(Document):
    first_name = StringField(required=True)
    last_name = StringField()
    email = EmailField(required=True)
    pass_hash = StringField(required=True)
    meta = {"db_alias": "todo", "collection": "Users"}
=======
>>>>>>> caa985d (refactoring for microservices arch):todo_service/app/db.py
