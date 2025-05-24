from datetime import datetime, timezone

from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from database import Base
from fastapi.testclient import TestClient
import pytest

from main import app
from models import Skills, Users
from routers.users import bcrypt_context

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return { "username": 'foxy', 'id': 1, 'role': 'admin'}

@pytest.fixture
def test_user():
    user = Users(
        username="foxy",
        email="123@gmail.com",
        password_hash=bcrypt_context.hash("testpassword"),
        role="admin",
        created_at=datetime.now(timezone.utc)
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user  # tất cả users sẽ được xóa sao sao khi hết phiên
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()


@pytest.fixture
def test_skill(test_user):
    skill = Skills(
        title="Learn FastAPI",
        description="Mastering FastAPI step by step",
        status="Learning",
        user_id=test_user.id,
        created_at=datetime.now(timezone.utc)
    )
    db = TestingSessionLocal()
    db.add(skill)
    db.commit()
    yield skill                                        #tất cả skill sẽ được xóa sao sao khi hết phiên
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM skills;"))
        connection.commit()