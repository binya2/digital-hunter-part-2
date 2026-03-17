import os

import uvicorn
from fastapi import FastAPI

from routers import targets, analytics, visualization, bonus

app = FastAPI(title="Digital Hunter API")

app.include_router(targets.router)
app.include_router(analytics.router)
app.include_router(visualization.router)
app.include_router(bonus.router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.environ.get('API_HOST', '0.0.0.0'),
        port=int(os.environ.get('API_PORT', 8000)),
        reload=True
    )