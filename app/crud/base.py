import ipaddress
from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.activity_log import ActivityLog
from app.schemas.facebook_data import ActivityLogCreate


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(self, obj: ipaddress, session: AsyncSession) -> ActivityLog:
        db_obj = await session.execute(select(self.model).where(self.model.ip_address == obj))
        db_obj = db_obj.scalar()
        if db_obj is None:
            raise HTTPException(status_code=404, detail="Объект не найден")
        return db_obj

    async def create(self, obj: ActivityLogCreate, session: AsyncSession) -> ActivityLog:
        obj_data = self.model(**obj.model_dump())
        session.add(obj_data)
        await session.commit()
        await session.refresh(obj_data)
        return obj_data

    async def is_unique_ip_address(self, obj: ipaddress, session: AsyncSession) -> bool:
        result = await session.execute(select(ActivityLog).where(ActivityLog.ip_address == obj))
        existing_ip_address = result.fetchone()
        return not existing_ip_address
