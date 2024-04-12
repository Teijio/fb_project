from pydantic import AnyHttpUrl, BaseModel, Field
from pydantic.json_schema import SkipJsonSchema
from pydantic.networks import IPvAnyAddress


class ActivityLogCreate(BaseModel):
    ip_address: SkipJsonSchema[IPvAnyAddress] = None
    user_agent: str = Field(..., alias="userAgent")
    pixel: str
    token: str
    fbclid: str
    fbc: str
    fbp: str

    class Config:
        from_attributes = True


class PixelTokenSchema(BaseModel):
    pixel: str
    token: str

    class Config:
        from_attributes = True


class KeitaroStatusIP(BaseModel):
    url: AnyHttpUrl = Field(
        ...,
        example="https://adnanhaider.site/keitaro?&status=lead&ip=127.0.0.1",
    )
