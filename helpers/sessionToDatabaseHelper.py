from database import SessionLocal
from fastapi import Depends, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def router(prefix, tag):
    router = APIRouter(
        prefix=prefix,
        tags=tag
    )
    return router