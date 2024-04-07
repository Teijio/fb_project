from typing import Optional
from pydantic import BaseModel, Field
from pydantic.networks import IPvAnyAddress


class ActivityLogCreate(BaseModel):
    pixel: str
    fbclid: str
    token: str
    user_agent: str = Field(..., alias="userAgent")
    fbc: str
    fbp: str
    _ip_address: Optional[IPvAnyAddress] = None


class PixelTokenSchema(BaseModel):
    pixel: str
    token: str
