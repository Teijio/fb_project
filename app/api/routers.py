from fastapi import APIRouter

from app.api.endpoints import activity_log_router

main_router = APIRouter()
main_router.include_router(activity_log_router, prefix="/activity_log", tags=["Activity logs"])
