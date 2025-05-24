from typing import Annotated
from fastapi import Depends, HTTPException, Request
from starlette import status
from pydantic import BaseModel, Field

from helpers.limiter import limiter
from helpers.userHelper import check_user_authentication
from .auth import get_current_user
from passlib.context import CryptContext

from helpers.sessionToDatabaseHelper import db_dependency, router

router = router('/user', ['user'])

user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=8, max_length=128)

@router.get('/', status_code=status.HTTP_200_OK)
@limiter.limit("30/minute")
async def get_user(request: Request, user: user_dependency, db: db_dependency):
    user = check_user_authentication(db, user, return_user=True)
    return user

@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
async def change_password(request: Request, user: user_dependency, db: db_dependency, user_verification: UserVerification):
    user_model = check_user_authentication(db, user, return_user=True)
    if not bcrypt_context.verify(user_verification.password, user_model.password_hash):
        raise HTTPException(status_code=401, detail='Authenticated failed')

    user_model.password_hash = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()