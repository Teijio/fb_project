import uvicorn
from fastapi import FastAPI

from app.api.httpx_client import on_shutdown, on_start_up
from app.api.routers import main_router
from app.core.config import settings

app = FastAPI(title=settings.app_title, on_startup=[on_start_up], on_shutdown=[on_shutdown])
app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
