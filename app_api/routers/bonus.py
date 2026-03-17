from fastapi import APIRouter

router = APIRouter(
    prefix="/api/analytics",
    tags=["Bonus"]
)


# 6
@router.get("/escape-patterns")
def get_escape_patterns():
    pass


# 7
@router.get("/meeting-events")
def get_meeting_events():
    pass
