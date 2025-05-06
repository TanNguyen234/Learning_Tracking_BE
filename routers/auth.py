from datetime import timedelta, datetime, timezone
from typing import Annotated
from pydantic import BaseModel
from fastapi import Depends, HTTPException

from helpers.sessionToDatabaseHelper import db_dependency, router
from models import Users
from passlib.context import CryptContext
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

router = router('/auth', ['auth'])

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password_hash):
        return False
    return user

class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,create_user_req: CreateUserRequest):
    create_user_model = Users(
        username=create_user_req.username,
        email=create_user_req.email,
        password_hash=bcrypt_context.hash(create_user_req.password),
        role=create_user_req.role,
        created_at=create_user_req.created_at
    )

    db.add(create_user_model)
    db.commit()
    return create_user_model

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('id')
        user_role = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return { 'username': username, 'id': user_id, 'user_role': user_role }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")

def create_access_token(username: str, id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': id, 'role': role}
    expire = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: db_dependency,):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}
