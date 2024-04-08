import ipaddress

from fastapi import APIRouter, Request, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.crud.activity_log import activity_log_crud
from app.schemas.facebook_data import ActivityLogCreate

router = APIRouter(prefix="/activity_log", tags=["Activity logs"])


@router.post("/create/")
async def create_new_request_info(
    activity_log: ActivityLogCreate,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    activity_log.ip_address = ipaddress.ip_address(request.client.host)
    is_unique_ip_address = activity_log_crud.is_unique_ip_address(activity_log.ip_address, session)
    if not await is_unique_ip_address:
        raise HTTPException(status_code=422, detail="Данный IP уже есть в базе")
    new_activity_log = await activity_log_crud.create(activity_log, session)
    return new_activity_log
