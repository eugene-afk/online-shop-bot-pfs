from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func

from . import Base
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    created_at = Column(DateTime, default=func.current_timestamp())