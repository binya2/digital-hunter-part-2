from fastapi import APIRouter

router = APIRouter(
    prefix="/api/targets",
    tags=["Targets"]
)


# 1
@router.get("/high-value-movement")
def get_high_value_target_movement():
    pass


# 3
@router.get("/new-targets")
def get_new_targets():
    pass
