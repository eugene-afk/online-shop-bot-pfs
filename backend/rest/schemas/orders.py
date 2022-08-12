from datetime import datetime
from decimal import Decimal
from typing import List
from pydantic import BaseModel, Field

from .products import ProductSchema, ProductSchemaXls
from models.order import OrderStatus
from .user import UserSchema

class OrderProductSchema(BaseModel):
    id: int
    qty: int
    total_price: Decimal = Field(
        decimal_places=2
    )
    order_id: int
    product: ProductSchema
    class Config:
        orm_mode = True

class OrderProductSchemaXls(BaseModel):
    product: ProductSchemaXls
    qty: int
    total_price: Decimal = Field(
        decimal_places=2
    )
    class Config:
        orm_mode = True

class OrderSchemaXls(BaseModel):
    id: int
    address: str
    shipping_option_id: str
    total_amount: Decimal = Field(
        decimal_places=2
    )
    shipping_price: Decimal = Field(
        decimal_places=2
    )
    order_status: str
    created_at: datetime
    updated_at: datetime 
    user_id: int
    username: str
    products: List[OrderProductSchemaXls]

    class Config:
        orm_mode = True

class OrderSchema(BaseModel):
    id: int
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str
    shipping_option_id: str
    total_amount: Decimal = Field(
        decimal_places=2
    )
    shipping_price: Decimal = Field(
        decimal_places=2
    )
    status: OrderStatus
    created_at: datetime
    updated_at: datetime 
    products: List[OrderProductSchema]
    user: UserSchema    
    class Config:
        orm_mode = True

class OrdersResponseSchema(BaseModel):
    orders: List[OrderSchema]
    is_admin: bool
    class Config:
        orm_mode = True
        
class UpdateOrderStatusSchema(BaseModel):
    order_id: int
    from_user_id: int
    user_id: int
    status: str