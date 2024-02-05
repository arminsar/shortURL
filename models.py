from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func

from database import Base


class ShortUrl(Base):
    __tablename__ = "short_urls"
    
    url = Column(String)
    shortcode = Column(String, primary_key=True, index=True)
    created = Column(TIMESTAMP, server_default=func.now())
    redirects_count = Column(Integer, default=0)
    last_redirect = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
