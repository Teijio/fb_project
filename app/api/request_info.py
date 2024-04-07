from fastapi import APIRouter

from app.crud.request_info import create_request_info
from app.schemas.facebook_data import RequestInfoCreate


router = APIRouter()

@router.post("/request_info/")
async def create_new_request_info(request_info: RequestInfoCreate):
    new_request_info = await create_request_info(request_info)
    return new_request_info