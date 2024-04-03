from fastapi import APIRouter

from app.crud.facebook_data import create_facebook_data
from app.schemas.facebook_data import FacebookDataCreate


router = APIRouter()

@router.post("/facebook_data/")
async def create_new_facebook_data(facebook_data: FacebookDataCreate):
    new_facebook_data = await create_facebook_data(facebook_data)
    return new_facebook_data