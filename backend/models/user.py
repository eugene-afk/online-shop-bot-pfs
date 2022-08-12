from sqlalchemy import Column, String, DateTime, Boolean, BigInteger 
from sqlalchemy.sql import func

from . import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(255))
    username = Column(String(255), default=None)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.current_timestamp())
