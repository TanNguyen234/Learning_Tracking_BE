from helpers.sessionToDatabaseHelper import get_db
from .utils import *
from routers.auth import authenticate_user, create_token, SECRET_KEY, ALGORITHM, get_current_user
from jose import jwt
from fastapi import HTTPException
from datetime import timedelta
import pytest

app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    auth_user =authenticate_user(test_user.username, password="testpassword", db=db)

    assert auth_user is not None
    assert auth_user.username == test_user.username

    auth_user_username_fail = authenticate_user("wrong_username", "testpassword", db)
    assert auth_user_username_fail == False

    auth_user_password_fail = authenticate_user(test_user.username, "wrong_password", db)
    assert auth_user_password_fail == False


@pytest.mark.asyncio
async def test_get_current_user_valid_token(test_user):
    encode = {'sub': 'foxy', 'id': 1, 'role': 'admin'}

    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {'username': 'foxy', 'id': 1, 'user_role': 'admin'}

def test_create_access_token(test_user):
    username = "testusername"
    user_id = 1
    role = 'user'
    exprires_delta = timedelta(days=1)
    token = create_token(username, user_id, role, exprires_delta)

    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_signature': False})
    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role

@pytest.mark.asyncio
async def test_get_current_user_missing_payload(test_user):
    encode = {'sub': 'user'}

    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as ecxinfo:
        await get_current_user(token=token)

    assert ecxinfo.value.status_code == 401
    assert ecxinfo.value.detail == 'Could not validate user.'


