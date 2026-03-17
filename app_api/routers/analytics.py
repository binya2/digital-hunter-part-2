from fastapi import APIRouter, HTTPException

from app_api.services import analytics

router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"]
)


# 2
@router.get("/signal-sources")
def get_signal_sources_analysis():
    result = analytics.signal_sources_analysis()
    if not result:
        raise HTTPException(status_code=404, detail="No signal sources data available")
    return result


# 4
@router.get("/sleeper-cells")
def get_sleeper_cells():
    result = analytics.sleeper_cells()
    if not result:
        raise HTTPException(status_code=404, detail="No sleeper cells (pattern changes) detected")
    return result
