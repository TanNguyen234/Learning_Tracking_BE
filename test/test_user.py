from fastapi import status
from helpers.sessionToDatabaseHelper import get_db
from routers.users import get_current_user
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get('/user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == "foxy"
    assert response.json()['email'] == "123@gmail.com"
    assert response.json()['role'] == "admin"
    print(response.json())

def test_change_password_success(test_user):
    response = client.put('/user/password', json={"password": "testpassword", "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_fail(test_user):
    response = client.put('/user/password', json={"password": "wrong_password", "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
