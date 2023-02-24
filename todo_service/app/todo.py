from fastapi import APIRouter, status, Depends, Form
from fastapi.exceptions import HTTPException
from models import TodosModel, TodosModelList
from db import StatusEnum, Todos

todos_router = APIRouter(prefix="/todos")


def convert_objectid_to_str(obj):
    obj["_id"] = str(obj["_id"])


@todos_router.post("/create")
async def create_todo(todo: TodosModel):
    todo = Todos(**todo.dict())
    todo.save()
    return {"detail": "todo saved successfully"}


@todos_router.get("/all", response_model=TodosModelList)
async def get_todos():
    todos = Todos.objects()
    todos = list(map(lambda s: s.to_mongo().to_dict(), todos))
    for i in todos:
        convert_objectid_to_str(i)
    todos = TodosModelList(todos=todos)
    return todos


@todos_router.get("/{id}", response_model=TodosModel)
async def get_todo(id: str):
    todo = Todos.objects(id=id)
    todo = todo[0].to_mongo().to_dict()
    convert_objectid_to_str(todo)
    return todo


@todos_router.put("/{id}/edit")
async def edit_todo(id: str, todo: TodosModel):
    t = Todos.objects(id=id).update_one(
        set__title=todo.title,
        set__desc=todo.desc,
        set__tags=todo.tags,
        set__flag=todo.flag,
        set__date=todo.date,
        set__time=todo.time,
        set__status=todo.status,
    )
    return {"detail": "todo updated"}


@todos_router.put("/{id}/edit/status")
async def edit_status(id: str, status: StatusEnum):
    todo = Todos.objects(id=id).update_one(
        set__status=status,
    )
    return {"detail": f"status updated to {status}"}


@todos_router.put("/{id}/delete")
async def delete_todo(id: str):
    todo = Todos.objects(id=id).delete()
    return {"detail": f"todo deleted {id}"}
