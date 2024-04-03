from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import INET

from app.core.database import Base


class FacebookData(Base):
    ip_address = Column(INET, unique=True, nullable=False)
    userAgent = Column(Text, nullable=False)
    pixel = Column(String(1000), nullable=False)
    token = Column(String(1000), nullable=False)
    fbclid = Column(String(1000))
    fbc = Column(String(1000), nullable=False)
    fbp = Column(String(1000), nullable=False)


class PixelToken(Base):
    pixel = Column(String(1000), unique=True, nullable=False)
    token = Column(String(1000), nullable=False)

    facebook_data = relationship("FacebookData", back_populates="pixel_token")


FacebookData.pixel_token = relationship("PixelToken", back_populates="facebook_data")
