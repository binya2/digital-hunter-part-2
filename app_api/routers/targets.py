from fastapi import APIRouter, HTTPException

from app_api.services import targets

router = APIRouter(
    prefix="/api/targets",
    tags=["Targets"]
)


# 1
@router.get("/high-value-movement")
def get_high_value_target_movement():
    result = targets.high_value_target_movement()
    if not result:
        raise HTTPException(status_code=404, detail="No high-value targets found with significant movement")
    return result


# 3
@router.get("/new-targets")
def get_new_targets():
    result = targets.new_targets()
    if not result:
        raise HTTPException(status_code=404, detail="No new targets found in the given timeframe")
    return result
