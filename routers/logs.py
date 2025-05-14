from datetime import datetime, timezone
from typing import List

from fastapi import HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status

from helpers.sessionToDatabaseHelper import db_dependency, router
from helpers.userHelper import check_user_authentication
from models import StudyLogs, Skills
from .users import user_dependency

router = router('/logs', ['logs'])

class LogRequest(BaseModel):
    skill_id: int = Field(gt=0)
    start_time: datetime
    end_time: datetime
    duration: int = Field(gt=0)
    note: str = Field(min_length=0, max_length=200)

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[LogRequest])
async def read_all_logs(user: user_dependency, db: db_dependency):
    check_user_authentication(db, user)
    skills = db.query(Skills).filter(Skills.user_id == user.get("id")).all()
    if not skills:
        raise HTTPException(status_code=404, detail="No skills found")

    skill_ids = [s.id for s in skills]
    logs = db.query(StudyLogs).filter(StudyLogs.skill_id.in_(skill_ids)).all()

    if not logs:
        raise HTTPException(status_code=404, detail="No logs found")

    return logs

@router.get('/{skill_id}', status_code=status.HTTP_200_OK, response_model=List[LogRequest])
async def read_log(user: user_dependency, db: db_dependency, skill_id: int = Path(gt=0)):
    check_user_authentication(db, user)
    log_model = db.query(StudyLogs).filter(StudyLogs.skill_id == skill_id, StudyLogs.user_id == user.get('id')).all()

    if log_model is None:
        raise HTTPException(status_code=404, detail='No log found')

    return log_model

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_log(user: user_dependency, db: db_dependency, log_request: LogRequest):
    check_user_authentication(db, user)

    log_model = StudyLogs(**log_request.model_dump(), user_id=user.get('id'), created_at=datetime.now(timezone.utc))

    db.add(log_model)
    db.commit()

@router.delete('/delete/{log_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_log(user: user_dependency, db: db_dependency, log_id: int = Path(gt=0)):
    check_user_authentication(db, user)

    log_model = db.query(StudyLogs).filter(StudyLogs.id == StudyLogs, StudyLogs.user_id == user.get('id')).first()

    if log_model is None:
        raise HTTPException(status_code=404, detail='Skill not found')

    db.query(StudyLogs).filter(StudyLogs.id == log_id).filter(StudyLogs.user_id == user.get('id')).delete()
    db.commit()

@router.patch("/update/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_log(user: user_dependency, db: db_dependency, log_request: LogRequest, skill_id: int = Path(gt=0)):
    check_user_authentication(db, user)

    log = db.query(StudyLogs).filter(StudyLogs.id == skill_id, StudyLogs.user_id == user.get('id')).first()
    if not log:
        raise HTTPException(status_code=404, detail="Skill not found")

    for key, value in log_request.model_dump(exclude_unset=True).items():
        setattr(log, key, value)

    db.commit()
