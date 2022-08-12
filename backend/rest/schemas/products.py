from decimal import Decimal
from pydantic import BaseModel, Field

class BaseSchema(BaseModel):
    id: int
    name: str

class ProductSchema(BaseSchema):    
    image_url: str
    stock_qty: int
    price: Decimal = Field(
        decimal_places=2
    )
    category_id: int

    class Config:
        orm_mode = True

class ProductSchemaXls(BaseSchema):
    pass

    class Config:
        orm_mode = True

class CategorySchema(BaseSchema):

    class Config:
        orm_mode = True