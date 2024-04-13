import ipaddress

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.httpx_client import Singletonhttpx
from app.api.utils import generate_facebook_event_data
from app.api.validators import (check_unique_ip_address, extract_keitaro_info,
                                get_activity_log, get_pixel_token)
from app.core.database import get_async_session
from app.crud.activity_log import activity_log_crud
from app.schemas.facebook_data import ActivityLogCreate, KeitaroStatusIP

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
    info_url: KeitaroStatusIP,
    session: AsyncSession = Depends(get_async_session),
):
    ip_address, status = extract_keitaro_info(info_url)
    activity_log = await get_activity_log(ip_address, session)
    pixel_token = await get_pixel_token(activity_log.pixel, session)
    facebook_data = generate_facebook_event_data(activity_log, status)
    result = await Singletonhttpx.send_data_to_facebook(pixel_token.pixel, pixel_token.token, facebook_data)
    return result
