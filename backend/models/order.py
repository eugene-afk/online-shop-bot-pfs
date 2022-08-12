from sqlalchemy import Column, String, Integer, DateTime, Numeric, Enum, BigInteger
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship, backref
import enum
from sqlalchemy.sql import func

from . import Base

class OrderStatus(enum.Enum):
    Unpaid = 0
    Pending = 1
    Sended = 2
    Delivered = 3

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    country_code = Column(String(10))
    state = Column(String(255))
    city = Column(String(255))
    street_line1 = Column(String(255))
    street_line2 = Column(String(255))
    post_code = Column(String(10))
    shipping_option_id = Column(String(255))
    total_amount = Column(Numeric(10, 2))
    shipping_price = Column(Numeric(10, 2))
    status = Column(Enum(OrderStatus), default=OrderStatus.Unpaid)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    products = relationship("OrderProduct", backref="order")
    user_id = Column(BigInteger, ForeignKey("users.id"))
    user = relationship("User")

class OrderProduct(Base):
    __tablename__ = 'order_products'
    id = Column(Integer, primary_key=True)
    qty = Column(Integer, default=1)
    total_price = Column(Numeric(10, 2))
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", backref=backref("orderproduct", uselist=False))