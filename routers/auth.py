from datetime import timedelta, datetime, timezone
from typing import Annotated
from pydantic import BaseModel
from fastapi import Depends, HTTPException

from helpers.limiter import limiter
from helpers.sessionToDatabaseHelper import db_dependency, router
from models import Users
from passlib.context import CryptContext
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
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

class Token(BaseModel):
    access_token: str
    token_type: str

class FullToken(Token):
    refresh_token: str

@router.post('/', status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
async def create_user(db: db_dependency,create_user_req: CreateUserRequest):
    create_user_model = Users(
        username=create_user_req.username,
        email=create_user_req.email,
        password_hash=bcrypt_context.hash(create_user_req.password),
        role='user',
        created_at=datetime.now(timezone.utc)
    )

    db.add(create_user_model)
    db.commit()
    return {
        "username": create_user_model.username,
        "email": create_user_model.email
    }

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('id')
        user_role = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return { 'username': username, 'id': user_id, 'user_role': user_role }
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired.")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")

def create_token(username: str, id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': id, 'role': role}
    expire = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/token", response_model=FullToken)
@limiter.limit("5/minute")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: db_dependency,):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    access_token = create_token(user.username, user.id, user.role, timedelta(minutes=30))
    refresh_token = create_token(user.username, user.id, user.role, timedelta(days=30))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,  # thêm dòng này
        "token_type": "bearer"
    }

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/refresh", response_model=Token)
@limiter.limit("10/minute")
async def refresh_access_token(req: RefreshRequest):
    try:
        payload = jwt.decode(req.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")
        user_role = payload.get("role")
        new_access_token = create_token(username, user_id, user_role, timedelta(minutes=30))
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired.")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token.")
