import uvicorn
from fastapi import FastAPI

from app.api.facebook_data import router
from app.core.config import settings

app = FastAPI(title=settings.app_title)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    # Команда на запуск uvicorn.
    # Здесь же можно указать хост и/или порт при необходимости,
    # а также другие параметры.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
