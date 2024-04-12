# import requests
# import time

# app/api/validators.py
import ipaddress
from typing import Optional, Union
from urllib.parse import parse_qs

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import activity_log_crud, pixel_token_crud
from app.models.activity_log import ActivityLog, PixelToken
from app.schemas.facebook_data import KeitaroStatusIP


async def get_pixel_token(pixel: str, session: AsyncSession) -> Optional[PixelToken]:
    pixel_token = await pixel_token_crud.get_by_attribute("pixel", pixel, session)
    if pixel_token is None:
        raise HTTPException(status_code=404, detail="Запись с данным pixel не найдена.")
    return pixel_token


async def get_activity_log(
    ip_address: ipaddress, session: AsyncSession
) -> Optional[ActivityLog]:
    activity_log = await activity_log_crud.get_by_attribute(
        "ip_address", ip_address, session
    )
    if activity_log is None:
        raise HTTPException(status_code=404, detail="Запись с данным IP не найдена.")
    return activity_log


async def check_unique_ip_address(ip_address: ipaddress, session: AsyncSession) -> None:
    is_unique_ip_address = activity_log_crud.is_unique_ip_address(ip_address, session)
    if not await is_unique_ip_address:
        raise HTTPException(status_code=422, detail="Данный IP уже есть в базе")


def extract_keitaro_info(
    info_url: KeitaroStatusIP,
) -> tuple[Union[ipaddress.IPv4Address, ipaddress.IPv6Address], str]:
    parsed_info_url = parse_qs(info_url.url.query)
    ip_address = parsed_info_url.get("ip", [None])[0]
    status = parsed_info_url.get("status", [None])[0]
    if ip_address is None or status is None:
        raise HTTPException(status_code=400, detail="IP/status не найдены.")
    if status not in ["lead", "sell"]:
        raise HTTPException(status_code=400, detail="Неверный статус.")
    try:
        formatted_ip_address = ipaddress.ip_address(ip_address)
    except ipaddress.AddressValueError as e:
        raise HTTPException(
            status_code=400, detail="Неверный формат IP адреса: " + str(e)
        )
    return formatted_ip_address, status
