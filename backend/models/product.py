from sqlalchemy import Column, String, Integer, Numeric, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from . import Base
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), default="Unknown", unique=True)
    image_url = Column(String(255))
    stock_qty = Column(Integer)
    price = Column(Numeric(10, 2))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp())
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category")
