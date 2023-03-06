from fastapi import FastAPI
from verify_token import token_routes

app = FastAPI()
app.include_router(token_routes, prefix="/api/v1")
