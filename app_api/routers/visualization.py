from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app_api.services import visualization

router = APIRouter(
    prefix="/api/visualization",
    tags=["Visualization"]
)


@router.get("/{entity_id}")
def plot_target_path(entity_id: str):
    image_bytes = visualization.generate_target_path_map(entity_id)

    if not image_bytes:
        raise HTTPException(status_code=404, detail="Entity not found or has no movement data")

    return Response(content=image_bytes, media_type="image/png")
