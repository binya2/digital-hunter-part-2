from fastapi import APIRouter

router = APIRouter(
    prefix="/api/visualization",
    tags=["Visualization"]
)


@router.get("/{entity_id}")
def plot_target_path(entity_id: str):
    pass
