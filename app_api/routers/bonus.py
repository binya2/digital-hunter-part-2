from fastapi import APIRouter, HTTPException

from app_api.services import bonus

router = APIRouter(
    prefix="/api/bonus",
    tags=["Bonus"]
)


# 6
@router.get("/escape-patterns")
def get_escape_patterns():
    result = bonus.escape_patterns()
    if not result:
        raise HTTPException(status_code=404, detail="No escape patterns detected after attacks")
    return result

# 7
@router.get("/meeting-events")
def get_meeting_events():
    result = bonus.meeting_events()
    if not result:
        raise HTTPException(status_code=404, detail="No escape patterns detected after attacks")
    return result
