import bcrypt
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db import User
from models import UserModel

user_routes = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="token")


def pass_hash(pwd: str):
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(str.encode(pwd), salt=salt)
    return hash


def decode_token(token: str):
    user = User.objects(email=token)
    user = UserModel(**user)
    return user


async def get_current_user(token: str = Depends(oauth2)):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication creentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@user_routes.get("/user/me")
async def user_me(user: UserModel = Depends(get_current_user)):
    return user


@user_routes.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = User.objects(email=form.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )
    user_model = UserModel(**user)
    hash_pass = pass_hash(form.password)
    if hash_pass != user.pass_hash:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    return {"access_token": user.email, "token_type": "bearer"}


@user_routes.post("/signup")
async def signup(form: UserModel):
    hash = pass_hash(form.pass_hash)
    user = User(
        first_name=form.first_name,
        last_name=form.last_name,
        email=form.email,
        pass_hash=hash,
        disabled=False,
    )
    user.save()
    return {"done": "done"}
