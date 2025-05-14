from pydantic import BaseModel
from datetime import datetime

class SkillResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class LogResponse(BaseModel):
    id: int
    user_id: int
    skill_id: int
    start_time: datetime
    end_time: datetime
    duration: int
    note: str
    created_at: datetime