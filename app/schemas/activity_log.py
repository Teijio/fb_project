from pydantic import BaseModel, Field, Json
from pydantic.json_schema import SkipJsonSchema
from pydantic.networks import IPvAnyAddress


class ActivityLogCreate(BaseModel):
    ip_address: SkipJsonSchema[IPvAnyAddress] = None
    user_agent: str = Field(..., alias="userAgent")
    pixel: str
    fbclid: str
    fbc: str
    sub_id: str
    flow: str
    fbp: str = None
    extra_data: SkipJsonSchema[Json] = None

    class Config:
        extra = "allow"
        from_attributes = True


class PixelTokenSchema(BaseModel):
    pixel: str
    token: str

    class Config:
        from_attributes = True
