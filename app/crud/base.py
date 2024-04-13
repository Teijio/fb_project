from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity_log import ActivityLog


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get_by_attribute(self, attr_name: str, attr_value: str, session: AsyncSession):
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(select(self.model).where(attr == attr_value))
        return db_obj.scalars().first()

    async def create(self, obj, session: AsyncSession) -> ActivityLog:
        obj_data = self.model(**obj.model_dump())
        session.add(obj_data)
        await session.commit()
        await session.refresh(obj_data)
        return obj_data
