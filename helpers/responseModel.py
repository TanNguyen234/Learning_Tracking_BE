from pydantic import BaseModel
from datetime import datetime
from typing import List

class PaginationMeta(BaseModel):
    current_page: int
    limit: int
    offset: int
    total_pages: int
    total_items: int

class SkillResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class SkillListResponse(BaseModel):
    data: List[SkillResponse]
    pagination: PaginationMeta

class LogResponse(BaseModel):
    id: int
    user_id: int
    skill_id: int
    skill_name: str
    start_time: datetime
    end_time: datetime
    duration: int
    note: str
    created_at: datetime

class ChartItem(BaseModel):
    date: datetime
    hours: float

class SkillPieItem(BaseModel):
    type: str  # Tên kỹ năng
    value: float  # Tổng số giờ học cho kỹ năng đó

class StatsResponse(BaseModel):
    totalHours: float
    totalSkills: int
    totalLogs: int
    chartData: List[ChartItem]
    skillPieData: List[SkillPieItem]