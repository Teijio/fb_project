import ipaddress

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.crud.activity_log import activity_log_crud
from app.schemas.facebook_data import ActivityLogCreate, KeitaroStatusIP
from app.api.validators import check_unique_ip_address

router = APIRouter()


@router.post("/create/")
async def create_new_request_info(
    activity_log: ActivityLogCreate,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    activity_log.ip_address = ipaddress.ip_address(request.client.host)
    await check_unique_ip_address(activity_log.ip_address, session)
    new_activity_log = await activity_log_crud.create(activity_log, session)
    return new_activity_log


@router.post("/find/")
async def find_request_info(
    keitaro_info: KeitaroStatusIP,
    session: AsyncSession = Depends(get_async_session),
):
    # data = await activity_log_crud.get(activity_log, )
    print(keitaro_info)
    pass
