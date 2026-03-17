import os

import uvicorn
from fastapi import FastAPI
from routers import targets, analytics, visualization

app = FastAPI(title="Digital Hunter API")

app.include_router(targets.router)
app.include_router(analytics.router)
app.include_router(visualization.router)


if __name__ == "__main__":
    uvicorn.run(
        "api_app.main:app",
        host=os.environ.get('API_HOST'),
        port=int(os.environ.get('API_PORT'))
    )