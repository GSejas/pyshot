
from sqlalchemy import Column, String, DateTime
from .database import Base
from datetime import datetime

class Screenshot(Base):
    __tablename__ = "screenshots"
    id = Column(String, primary_key=True, index=True)
    filename = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)