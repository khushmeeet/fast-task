import os
import datetime
import time
import json
import httpx
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv
from db import User
from models import UserModel, JWTModel

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

user_routes = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login", scheme_name="JWT")
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pwd(pwd: str):
    return pwd_ctx.hash(pwd)


def verify_hash_pwd(pwd: str, hash: str):
    return pwd_ctx.verify(pwd, hash)


def decode_token(token: str):
    user = User.objects(email=token)
    user = UserModel(**user)
    return user


def create_jwt(data: dict, expires_delta: int | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = time.time() + expires_delta
    else:
        expire = time.time() + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2)):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"http://token-service:8080/api/v1/verify/token", json={"token": token}
        )
        resp = json.loads(resp.content)
        if resp["condition"] == False:
            if "expired" in resp["detail"]:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="JWT expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            if "invalid" in resp["detail"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        else:
            user = User.objects(email=resp.get("email"))
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return user[0].to_mongo().to_dict()


@user_routes.get("/user/me", response_model=UserModel)
async def user_me(user: UserModel = Depends(get_current_user)):
    return user


@user_routes.post("/login", response_model=JWTModel)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = User.objects(email=form.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_model = UserModel(
        first_name=user[0].first_name,
        last_name=user[0].last_name,
        email=user[0].email,
        pass_hash=user[0].pass_hash,
    )
    if not verify_hash_pwd(form.password, user_model.pass_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    jwt = create_jwt(
        data={"email": user_model.email}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return {"access_token": jwt, "token_type": "bearer"}


@user_routes.post("/signup")
async def signup(form: UserModel):
    user = User.objects(email=form.email).values_list()
    if len(user) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    hash = hash_pwd(form.pass_hash)
    user = User(
        first_name=form.first_name,
        last_name=form.last_name,
        email=form.email,
        pass_hash=hash,
    )
    user.save()
    return {"detail": "user registered successfully"}


@user_routes.post("/logout")
async def logout(auth: str):
    return {"detail": "token revoked"}
