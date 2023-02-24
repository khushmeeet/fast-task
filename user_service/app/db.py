from mongoengine import (
    Document,
    StringField,
    EmailField,
)


class User(Document):
    first_name = StringField(required=True)
    last_name = StringField()
    email = EmailField(required=True)
    pass_hash = StringField(required=True)
    meta = {"db_alias": "todo", "collection": "Users"}
