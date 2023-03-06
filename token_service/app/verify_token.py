import os
import datetime
from fastapi import APIRouter
from jose import JWTError, jwt
from dotenv import load_dotenv
from models import VerifyTokenResponseModel, TokenModel

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default")
ALGORITHM = "HS256"

token_routes = APIRouter()


@token_routes.post("/verify/token", response_model=VerifyTokenResponseModel)
async def verify_token(token: TokenModel):
    try:
        payload = jwt.decode(token.token, SECRET_KEY, algorithms=[ALGORITHM])
        if datetime.datetime.fromtimestamp(payload["exp"]) < datetime.datetime.now():
            return {"detail": "JWT expired", "condition": False}
        else:
            return {
                "detail": "JWT valid",
                "condition": True,
                "email": payload.get("email"),
            }
    except JWTError as e:
        return {"detail": "JWT invalid", "condition": False}
