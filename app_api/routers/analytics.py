from fastapi import APIRouter

from app_api.services import analytics

router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"]
)


# 2
@router.get("/signal-sources")
def get_signal_sources_analysis():
    return analytics.signal_sources_analysis()


# 4
@router.get("/sleeper-cells")
def get_sleeper_cells():
    return analytics.sleeper_cells()
