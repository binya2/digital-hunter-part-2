from fastapi import APIRouter

from app_api.services import targets

router = APIRouter(
    prefix="/api/targets",
    tags=["Targets"]
)


# 1
@router.get("/high-value-movement")
def get_high_value_target_movement():
    return targets.high_value_target_movement()


# 3
@router.get("/new-targets")
def get_new_targets():
    return targets.new_targets()
