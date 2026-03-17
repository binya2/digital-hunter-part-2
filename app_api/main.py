import os

import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "api_app.main:app",
        host=os.environ.get('API_HOST'),
        port=int(os.environ.get('API_PORT'))
    )