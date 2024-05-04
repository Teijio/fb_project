# import requests
# import time

# app/api/validators.py
import ipaddress
from typing import Optional, Union
from urllib.parse import parse_qs

from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import activity_log_crud, application_crud, flow_params_crud, pixel_token_crud
from app.models.activity_log import ActivityLog, Application, FlowParams, PixelToken


async def get_pixel_token(pixel: str, session: AsyncSession) -> Optional[PixelToken]:
    pixel_token = await pixel_token_crud.get_by_attribute("pixel", pixel, session)
    if pixel_token is None:
        raise HTTPException(status_code=404, detail="Запись с данным pixel не найдена")
    return pixel_token


async def get_activity_log_by_ip(ip_address: ipaddress, session: AsyncSession) -> Optional[ActivityLog]:
    activity_log = await activity_log_crud.get_by_attribute("ip_address", ip_address, session)
    if activity_log is None:
        raise HTTPException(status_code=404, detail="Запись с данным IP не найдена")
    return activity_log


async def check_unique_ip_address(ip_address: ipaddress, session: AsyncSession) -> None:
    is_unique_ip_address = activity_log_crud.is_unique_ip_address(ip_address, session)
    if not await is_unique_ip_address:
        raise HTTPException(status_code=422, detail="Данный IP уже есть в базе")


def get_user_ip(request: Request) -> Union[ipaddress.IPv4Address, ipaddress.IPv6Address]:
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        ip_address = forwarded_for.split(",")[-1].strip()
    else:
        ip_address = request.client.host
    if ip_address is None:
        raise HTTPException(status_code=422, detail="IP адрес отсутствует в запросе")
    return ipaddress.ip_address(ip_address)


def extract_keitaro_info(
    info_url: str,
) -> tuple[Union[ipaddress.IPv4Address, ipaddress.IPv6Address], str]:
    parsed_info_url = parse_qs(info_url)
    ip_address = parsed_info_url.get("ip", [None])[0]
    status = parsed_info_url.get("status", [None])[0]
    if ip_address is None or status is None:
        raise HTTPException(status_code=400, detail="IP/status не найдены")
    if status not in ["lead", "sale"]:
        raise HTTPException(status_code=400, detail="Неверный статус")
    try:
        formatted_ip_address = ipaddress.ip_address(ip_address)
    except ipaddress.AddressValueError as e:
        raise HTTPException(status_code=400, detail="Неверный формат IP адреса: " + str(e))
    return formatted_ip_address, status


async def match_activity_log_and_flow(
    ip_address: ipaddress, session: AsyncSession
) -> Optional[tuple[ActivityLog, FlowParams]]:
    activity_log = await activity_log_crud.get_by_attribute("ip_address", ip_address, session)
    if activity_log is None:
        return None, None
    flow_params = await flow_params_crud.get_by_attribute("flow", activity_log.flow, session)
    return activity_log, flow_params


async def get_application(app: str, session: AsyncSession) -> Optional[Application]:
    application = await application_crud.get_by_attribute("application", app, session)
    if not application:
        raise HTTPException(status_code=404, detail="app не найден")
    return application
