from fastapi import APIRouter

from app_api.services import bonus

router = APIRouter(
    prefix="/api/bonus",
    tags=["Bonus"]
)


# 6
@router.get("/escape-patterns")
def get_escape_patterns():
    return bonus.escape_patterns()


# 7
@router.get("/meeting-events")
def get_meeting_events():
    pass
