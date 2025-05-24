from collections import defaultdict
from fastapi import HTTPException, Request
from starlette import status

from helpers.limiter import limiter
from helpers.responseModel import StatsResponse
from helpers.sessionToDatabaseHelper import db_dependency, router
from helpers.userHelper import check_user_authentication
from models import Skills, StudyLogs
from .users import user_dependency

router = router('/stats', ['stats'])

@router.get('/', status_code=status.HTTP_200_OK, response_model=StatsResponse)
@limiter.limit("10/minute")
async def read_stats(request: Request, user: user_dependency, db: db_dependency):
    check_user_authentication(db, user)

    skills = db.query(Skills).filter(Skills.user_id == user.get("id")).all()
    logs = db.query(StudyLogs).filter(StudyLogs.user_id == user.get("id")).all()

    if not skills and not logs:
        raise HTTPException(status_code=404, detail='No stats found')

    # Tính tổng giờ học
    total_hours = sum(log.duration for log in logs) / 3600  # nếu duration là giây, đổi sang giờ

    # Tính chartData: tổng thời gian học theo từng ngày
    chart_dict = defaultdict(float)
    for log in logs:
        date_str = log.start_time.date()
        chart_dict[date_str] += log.duration / 3600

    chart_data = [
        {"date": date, "hours": round(hours, 2)} for date, hours in sorted(chart_dict.items())
    ]

    # Tính skillPieData: tổng thời gian học theo từng kỹ năng
    skill_dict = defaultdict(float)
    skill_map = {s.id: s.title for s in skills}
    for log in logs:
        skill_title = skill_map.get(log.skill_id, "Unknown")
        skill_dict[skill_title] += log.duration / 3600

    skill_pie_data = [
        {"type": title, "value": round(hours, 2)} for title, hours in skill_dict.items()
    ]

    return {
        "totalHours": round(total_hours, 2),
        "totalSkills": len(skills),
        "totalLogs": len(logs),
        "chartData": chart_data,
        "skillPieData": skill_pie_data,
    }