from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text, Integer
from sqlalchemy.dialects.postgresql import INET, JSONB

from app.core.database import Base

SUB_ID_1 = "sub_id_1"


class ActivityLog(Base):
    ip_address = Column(INET, unique=True, nullable=False, index=True)
    user_agent = Column(Text, nullable=False)
    pixel = Column(String(30), nullable=False)
    fbclid = Column(String(1000), nullable=False)
    fbc = Column(String(1000), nullable=False)
    fbp = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    flow = Column(String(255), nullable=False)
    extra_data = Column(JSONB, nullable=True)
    flag = Column(Integer, nullable=True)

    @property
    def params_format(self):
        return {SUB_ID_1: self.id, **self.extra_data}


class FlowParams(Base):
    flow = Column(String(255), nullable=True, index=True)
    url = Column(String(100), nullable=True)
    from_who = Column(String(1000), nullable=True)


class PixelToken(Base):
    pixel = Column(String(30), unique=True, nullable=False, index=True)
    token = Column(String(1000), nullable=False)


class Application(Base):
    application = Column(String(250), nullable=False, index=True)
    url = Column(String(250), nullable=False)
