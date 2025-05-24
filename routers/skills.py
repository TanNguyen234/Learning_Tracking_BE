from datetime import datetime, timezone

from fastapi import HTTPException, Path, Request
from fastapi.params import Query
from pydantic import BaseModel, Field
from starlette import status

from helpers.limiter import limiter
from helpers.pagination import paginate
from helpers.responseModel import SkillResponse, SkillListResponse
from helpers.sessionToDatabaseHelper import db_dependency, router
from helpers.userHelper import check_user_authentication
from models import Skills
from .users import user_dependency

router = router('/skills', ['skills'])

class SkillRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    status: str = Field(default="Learning")

@router.get('/', status_code=status.HTTP_200_OK, response_model=SkillListResponse)
@limiter.limit("30/minute")
async def read_all_skill(
        request: Request,
        user: user_dependency,
        db: db_dependency,
        current_page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1)
):
    check_user_authentication(db, user)

    skills = db.query(Skills).filter(Skills.user_id == user.get('id')).all()

    if len(skills) == 0:
        raise HTTPException(status_code=404, detail='Skill not found')

    pagination_info = paginate(current_page, limit, len(skills))

    paginated_skills = skills[pagination_info["offset"]: pagination_info["offset"] + limit]

    return {
        "data": paginated_skills,
        "pagination": pagination_info
    }

@router.get('/{skill_id}', status_code=status.HTTP_200_OK, response_model=SkillResponse)
@limiter.limit("30/minute")
async def read_skill(request: Request, user: user_dependency, db: db_dependency, skill_id: int = Path(gt=0)):
    check_user_authentication(db, user)
    skill_model = db.query(Skills).filter(Skills.id == skill_id, Skills.user_id == user.get('id')).first()

    if skill_model is None:
        raise HTTPException(status_code=404, detail='Skill not found')

    return skill_model

@router.post("/create", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def create_skill(request: Request, user: user_dependency, db: db_dependency, skill_request: SkillRequest):
    check_user_authentication(db, user)

    skill_model = Skills(**skill_request.model_dump(), user_id=user.get('id'), created_at=datetime.now(timezone.utc))

    db.add(skill_model)
    db.commit()

@router.delete('/delete/{skill_id}', status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/minute")
async def delete_skill(request: Request, user: user_dependency, db: db_dependency, skill_id: int = Path(gt=0)):
    check_user_authentication(db, user)

    skill_model = db.query(Skills).filter(Skills.id == skill_id and Skills.user_id == user.get('id')).first()

    if skill_model is None:
        raise HTTPException(status_code=404, detail='Skill not found')

    db.query(Skills).filter(Skills.id == skill_id).filter(Skills.user_id == user.get('id')).delete()
    db.commit()

@router.patch("/update/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/minute")
async def update_skill(request: Request, user: user_dependency, db: db_dependency, skill_request: SkillRequest, skill_id: int = Path(gt=0)):
    check_user_authentication(db, user)

    skill = db.query(Skills).filter(Skills.id == skill_id, Skills.user_id == user.get('id')).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    for key, value in skill_request.model_dump(exclude_unset=True).items():
        setattr(skill, key, value)

    db.commit()
