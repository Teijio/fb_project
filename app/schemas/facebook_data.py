from pydantic import BaseModel


class RequestInfoBase(BaseModel):
    ip_address: str
    user_agent: str
    pixel: str
    token: str
    fbclid: str = None
    fbc: str
    fbp: str


class RequestInfoCreate(RequestInfoBase):
    pass
