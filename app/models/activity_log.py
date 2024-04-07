from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import INET

from app.core.database import Base


class ActivityLog(Base):
    ip_address = Column(INET, unique=True, nullable=False, index=True)
    user_agent = Column(Text, nullable=False)
    pixel = Column(String(1000), nullable=False)
    token = Column(String(1000), nullable=False)
    fbclid = Column(String(1000), nullable=False)
    fbc = Column(String(1000), nullable=False)
    fbp = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)


class PixelToken(Base):
    pixel = Column(String(1000), unique=True, nullable=False)
    token = Column(String(1000), nullable=False)

