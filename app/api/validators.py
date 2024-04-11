# app/api/validators.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from app.crud.activity_log import activity_log_crud
from app.models.activity_log import ActivityLog


async def check_activity_log_exists(activity_log_ip_address: int, session: AsyncSession) -> ActivityLog:
    activity_log = await activity_log_crud.get(activity_log_ip_address, session)
    if activity_log is None:
        raise HTTPException(status_code=404, detail="Запись с данным IP не найдена.")
    return activity_log


async def check_unique_ip_address(activity_log_ip_address: int, session: AsyncSession) -> None:
    is_unique_ip_address = activity_log_crud.is_unique_ip_address(activity_log_ip_address, session)
    if not await is_unique_ip_address:
        raise HTTPException(status_code=422, detail="Данный IP уже есть в базе")
