from fastapi import status
from helpers.sessionToDatabaseHelper import get_db
from routers.users import get_current_user
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_create_skill_success(test_user):
    response = client.post("/skills/create", json={
        "title": "Python",
        "description": "Learn Python programming",
        "status": "Learning"
    })
    assert response.status_code == status.HTTP_201_CREATED

def test_read_all_skills(test_skill):
    response = client.get("/skills/?current_page=1&limit=10")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data["data"], list)
    assert data["pagination"]["current_page"] == 1
    assert len(data["data"]) >= 1

def test_read_skill_by_id_success(test_skill):
    response = client.get(f"/skills/{test_skill.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == test_skill.title

def test_read_skill_by_id_not_found(test_skill):
    response = client.get("/skills/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_skill_success(test_skill):
    response = client.patch(f"/skills/update/{test_skill.id}", json={
        "title": "Updated Title",
        "description": "Updated description",
        "status": "Done"
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_update_skill_not_found(test_skill):
    response = client.patch("/skills/update/999999", json={
        "title": "No skill",
        "description": "This skill does not exist",
        "status": "Done"
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_skill_success(test_skill):
    response = client.delete(f"/skills/delete/{test_skill.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_skill_not_found(test_skill):
    response = client.delete("/skills/delete/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
