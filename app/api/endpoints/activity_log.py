import ipaddress
import logging
import urllib.parse

from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import RedirectResponse
from pydantic.networks import IPvAnyAddress
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.httpx_client import Singletonhttpx
from app.api.utils import generate_facebook_event_data
from app.api.validators import (
    check_unique_ip_address,
    extract_keitaro_info,
    get_activity_log_by_ip,
    get_application,
    get_pixel_token,
    get_user_ip,
    match_activity_log_and_flow,
)
from app.core.config import settings
from app.core.database import get_async_session
from app.crud import activity_log_crud
from app.schemas.activity_log import ActivityLogCreate

router = APIRouter()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(settings.logs_file_path_prod)  # переключить на прод
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)


URL = "https://agengy88dol.online/"


@router.post("/create/")
async def create_new_request_info(
    activity_log: ActivityLogCreate,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):

    activity_log.ip_address = ipaddress.ip_address(get_user_ip(request))
    activity_log.extra_data = activity_log.model_extra.copy()
    activity_log.model_extra.clear()
    logger.info(f"facebook_log >>> {activity_log}")
    await check_unique_ip_address(activity_log.ip_address, session)
    new_activity_log = await activity_log_crud.create(activity_log, session)
    logger.info("facebook_log успешно создан")
    return new_activity_log


# async def find_request_info(info_url: str = Body(...), session: AsyncSession = Depends(get_async_session)):
@router.get("/find_fb/")
async def find_request_info(
    status: str, ip_address: IPvAnyAddress, session: AsyncSession = Depends(get_async_session)
):
    # logger.info(f"keitaro_URL >>> {info_url}")
    # ip_address, status = extract_keitaro_info(info_url)
    activity_log = await get_activity_log_by_ip(ip_address, session)
    pixel_token = await get_pixel_token(activity_log.pixel, session)
    facebook_data = generate_facebook_event_data(activity_log, status)
    result = await Singletonhttpx.send_data_to_facebook(pixel_token.pixel, pixel_token.token, facebook_data)
    logger.info(f"facebook_data_keitaro_POST >>> {facebook_data}")
    logger.info(f"facebook_RESULT >>> {result}")
    return result


@router.get("/find_flow/", response_class=RedirectResponse)
async def find_flow(ip_address: IPvAnyAddress, app: str, session: AsyncSession = Depends(get_async_session)):
    activity_log, flow = await match_activity_log_and_flow(ip_address, session)
    if flow:
        pixel_token = await get_pixel_token(activity_log.pixel, session)
        facebook_data = generate_facebook_event_data(activity_log)
        result = await Singletonhttpx.send_data_to_facebook(pixel_token.pixel, pixel_token.token, facebook_data)
        logger.info(f"facebook_data_flow_POST >>> {facebook_data}")
        logger.info(f"facebook_RESULT >>> {result}")
        params = urllib.parse.urlencode(activity_log.params_format)
        url_for_redirect = f"{URL}{flow.url}?{params}"
        logger.info(f"redirect_url_FLOW >>> {url_for_redirect}")
        return RedirectResponse(url_for_redirect)
    application = await get_application(app, session)
    url_for_redirect = f"{URL}{application.url}"
    logger.info(f"redirect_url_APP >>> {url_for_redirect}")
    return RedirectResponse(url_for_redirect)
