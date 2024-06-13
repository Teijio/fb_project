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

    async def update_flag_by_ip(self, obj: ipaddress, session: AsyncSession, action: str = "flow_matched"):
        db_obj = await self.get_by_attribute("ip_address", obj, session)
        if not db_obj:
            return None

        if action == "flow_matched":
            db_obj.flag = 1
        elif action == "lead":
            db_obj.flag = 2
        elif action == "sale":
            db_obj.flag = 3
        else:
            raise ValueError("Invalid action value")

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


activity_log_crud = CRUDActivityLog(ActivityLog)
