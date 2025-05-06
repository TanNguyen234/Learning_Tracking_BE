from fastapi import HTTPException
from models import Users

def check_user_authentication(db, user, return_user=False):
    if user is None:
        raise HTTPException(status_code=401, detail='Authenticated failed')

    user_model = db.query(Users).filter(Users.id == user['id']).first()

    if user_model is None:
        raise HTTPException(status_code=401, detail='Authenticated failed')

    if return_user:
        return user_model