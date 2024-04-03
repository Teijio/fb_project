from pydantic import BaseModel


class FacebookDataBase(BaseModel):
    # ip_address: str
    userAgent: str
    pixel: str
    token: str
    fbclid: str = None
    fbc: str
    fbp: str


class FacebookDataCreate(FacebookDataBase):
    pass
