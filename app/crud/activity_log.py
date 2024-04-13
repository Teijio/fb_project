import ipaddress

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.activity_log import ActivityLog


class CRUDActivityLog(CRUDBase):
    async def is_unique_ip_address(self, obj: ipaddress, session: AsyncSession) -> bool:
        result = await session.execute(select(ActivityLog).where(ActivityLog.ip_address == obj))
        existing_ip_address = result.fetchone()
        return not existing_ip_address


activity_log_crud = CRUDActivityLog(ActivityLog)
