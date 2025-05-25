from fastapi import status
from helpers.sessionToDatabaseHelper import get_db
from routers.users import get_current_user
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_logs(test_log):
    response = client.get("/logs")
    assert response.status_code == status.HTTP_200_OK

def test_read_logs_success(test_log):
    response = client.get("/logs/1")
    assert response.status_code == status.HTTP_200_OK

def test_read_logs_not_exist_id(test_log):
    response = client.get("/logs/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_log_success(test_skill):
    response = client.post("/logs/create", json={
        "skill_id": test_skill.id,
        "start_time": "2025-04-20 08:00:00",
        "end_time": "2025-04-20 08:00:00",
        "duration": 0,
        "note": "If you don't believe in yourself how can you expect others believe in you!",
    })
    assert response.status_code == status.HTTP_201_CREATED

def test_create_log_invalid_value_request(test_skill):
    response = client.post("/logs/create", json={
        "skill_id": -1,
        "start_time": "2025-04-20 08:00:00",
        "end_time": "2025-04-20 08:00:00",
        "duration": -1,
        "note": "If you don't believe in yourself how can you expect others believe in you!",
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_delete_log_success(test_log):
    response = client.delete(f"/logs/delete/{test_log.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_log_not_found(test_log):
    response = client.delete("/logs/delete/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_log_success(test_log):
    response = client.patch(f"/logs/update/{test_log.id}", json={
        "skill_id": 1,
        "duration": 10,
        "note": "Be patient be confident and be successful"
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_update_log_not_found(test_log):
    response = client.patch("/logs/update/999999", json={
        "skill_id": 1,
        "duration": 10,
        "note": "Be patient"
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND