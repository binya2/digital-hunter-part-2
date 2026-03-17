from fastapi import APIRouter

router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"]
)


# 2
@router.get("/signal-sources")
def get_signal_sources_analysis():
    pass


# 4
@router.get("/sleeper-cells")
def get_sleeper_cells():
    pass
