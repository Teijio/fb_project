from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema
from pydantic.networks import IPvAnyAddress


class ActivityLogCreate(BaseModel):
    ip_address: SkipJsonSchema[IPvAnyAddress] = None
    user_agent: str = Field(..., alias="userAgent")
    pixel: str
    fbclid: str
    fbc: str
    fbp: str = None

    class Config:
        from_attributes = True


class PixelTokenSchema(BaseModel):
    pixel: str
    token: str

    class Config:
        from_attributes = True
