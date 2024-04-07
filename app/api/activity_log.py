from fastapi import APIRouter, Request

from app.crud.activity_log import create_activity_log
from app.schemas.facebook_data import ActivityLogCreate

router = APIRouter()


@router.post("/request_info/create/")
async def create_new_request_info(request_info: ActivityLogCreate, request: Request):
    client_host = request.client.host
    request_info._ip_address = client_host
    new_request_info = await create_activity_log(request_info)
    return new_request_info
