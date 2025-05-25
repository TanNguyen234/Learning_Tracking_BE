from datetime import datetime, timezone
from typing import List

from fastapi import HTTPException, Path, Request
from pydantic import BaseModel, Field
from starlette import status

from helpers.limiter import limiter
from helpers.sessionToDatabaseHelper import db_dependency, router
from helpers.userHelper import check_user_authentication
from models import StudyLogs, Skills
from .users import user_dependency

router = router('/logs', ['logs'])

class LogRequest(BaseModel):
    skill_id: int = Field(ge=0)
    start_time: datetime | None = None
    end_time: datetime | None = None
    duration: int | None = None
    note: str | None = None

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[LogRequest])
@limiter.limit("5/minute")
async def read_all_logs(request: Request, user: user_dependency, db: db_dependency):
    check_user_authentication(db, user)
    skills = db.query(Skills).filter(Skills.user_id == user.get("id")).all()
    if not skills:
        raise HTTPException(status_code=404, detail="No skills found")

    skill_ids = [s.id for s in skills]
    logs_with_skills = (
        db.query(
            StudyLogs,
            Skills.title.label("skill_name")
        )
        .join(Skills, StudyLogs.skill_id == Skills.id)
        .filter(StudyLogs.skill_id.in_(skill_ids))
        .all()
    )

    if not logs_with_skills:
        raise HTTPException(status_code=404, detail="No logs found")

    result = []
    for log, skill_name in logs_with_skills:
        log_data = {
            "id": log.id,
            "user_id": log.user_id,
            "skill_id": log.skill_id,
            "skill_name": skill_name,
            "start_time": log.start_time,
            "end_time": log.end_time,
            "duration": log.duration,
            "note": log.note,
            "created_at": log.created_at,
        }
        result.append(log_data)

    return result

@router.get('/{skill_id}', status_code=status.HTTP_200_OK, response_model=List[LogRequest])
async def read_log(request: Request, user: user_dependency, db: db_dependency, skill_id: int = Path(gt=0)):
    check_user_authentication(db, user)
    log_model = db.query(StudyLogs).filter(StudyLogs.skill_id == skill_id, StudyLogs.user_id == user.get('id')).all()

    if not log_model:
        raise HTTPException(status_code=404, detail='No log found')

    return log_model

@router.post("/create", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def create_log(request: Request, user: user_dependency, db: db_dependency, log_request: LogRequest):
    check_user_authentication(db, user)

    log_model = StudyLogs(**log_request.model_dump(), user_id=user.get('id'), created_at=datetime.now(timezone.utc))

    db.add(log_model)
    db.commit()

@router.delete('/delete/{log_id}', status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/minute")
async def delete_log(request: Request, user: user_dependency, db: db_dependency, log_id: int = Path(gt=0)):
    check_user_authentication(db, user)

    log_model = db.query(StudyLogs).filter(StudyLogs.id == log_id, StudyLogs.user_id == user.get('id')).first()

    if log_model is None:
        raise HTTPException(status_code=404, detail='Log not found')

    db.query(StudyLogs).filter(StudyLogs.id == log_id).filter(StudyLogs.user_id == user.get('id')).delete()
    db.commit()

@router.patch("/update/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/minute")
async def update_log(request: Request, user: user_dependency, db: db_dependency, log_request: LogRequest, log_id: int = Path(gt=0)):
    check_user_authentication(db, user)
    print(log_request, log_id)
    log = db.query(StudyLogs).filter(StudyLogs.id == log_id, StudyLogs.user_id == user.get('id')).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    for key, value in log_request.model_dump(exclude_unset=True).items():
        setattr(log, key, value)

    db.commit()
