import logging
import ipaddress

from fastapi import APIRouter, Body, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.httpx_client import Singletonhttpx
from app.api.utils import generate_facebook_event_data
from app.api.validators import check_unique_ip_address, extract_keitaro_info, get_activity_log, get_pixel_token
from app.core.database import get_async_session
from app.crud.activity_log import activity_log_crud
from app.schemas.facebook_data import ActivityLogCreate, KeitaroStatusIP

router = APIRouter()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler("/app/logs/logs.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)


@router.post("/create/")
async def create_new_request_info(
    activity_log: ActivityLogCreate,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        ip_address = forwarded_for.split(",")[-1].strip()
    else:
        ip_address = request.client.host
    activity_log.ip_address = ipaddress.ip_address(ip_address)
    logger.info(f"facebook_log >>> {activity_log}")
    await check_unique_ip_address(activity_log.ip_address, session)
    new_activity_log = await activity_log_crud.create(activity_log, session)
    return new_activity_log


@router.post("/check_ip/")
async def log_request(request: Request):
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return f"X_forwarded IP {forwarded_for.split(",")[-1].strip()} IP {request.client.host}"

    return f"IP {request.client.host}"


@router.post("/find/")
async def find_request_info(
    info_url: str = Body(...),
    session: AsyncSession = Depends(get_async_session),
):  
    logger.info(f"keitaro_URL >>> {info_url}")
    ip_address, status = extract_keitaro_info(info_url)
    activity_log = await get_activity_log(ip_address, session)
    pixel_token = await get_pixel_token(activity_log.pixel, session)
    facebook_data = generate_facebook_event_data(activity_log, status)
    logger.info(f"keitaro_POST >>> {info_url}")
    result = await Singletonhttpx.send_data_to_facebook(pixel_token.pixel, pixel_token.token, facebook_data)
    logger.info(f"keitaro_RESULT >>> {info_url}")
    return result
