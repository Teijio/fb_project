from pydantic import BaseModel, Field
from pydantic.networks import IPvAnyAddress
from pydantic.json_schema import SkipJsonSchema


class ActivityLogCreate(BaseModel):
    ip_address: SkipJsonSchema[IPvAnyAddress] = None
    user_agent: str = Field(..., alias="userAgent")
    pixel: str
    token: str
    fbclid: str
    fbc: str
    fbp: str

    class Config:
        orm_mode = True


class PixelTokenSchema(BaseModel):
    pixel: str
    token: str

    class Config:
        orm_mode = True
