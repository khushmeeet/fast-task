import os
from fastapi import FastAPI
from mongoengine import connect, disconnect
from dotenv import load_dotenv
from todo import todos_router

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

app = FastAPI()
app.include_router(todos_router, prefix="/api/v1/")


@app.on_event("startup")
async def startup():
    connect(host=MONGO_URI, alias="todo")


@app.on_event("shutdown")
async def shutdown():
    disconnect(alias="todo")
