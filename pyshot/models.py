
from sqlalchemy import Column, String, DateTime
from .database import Base
from datetime import datetime


class Screenshot(Base):
    """
    Represents a screenshot record in the database.

    Attributes:
        id (str): The unique identifier for the screenshot.
        filename (str): The name of the screenshot file.
        timestamp (datetime): The time when the screenshot was taken, defaults to the current UTC time.
    """
    __tablename__ = "screenshots"
    id = Column(String, primary_key=True, index=True)
    filename = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)