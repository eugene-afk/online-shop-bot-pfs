from typing import List
from fastapi import APIRouter, Depends

from ..services.products import ProductsService
from ..schemas.products import ProductSchema, CategorySchema

router = APIRouter(
    prefix='/products',
    tags=['Products'],
)

@router.get('/', response_model=List[ProductSchema])
async def get_products(search: str = "", category_id: int = 0, service: ProductsService = Depends()):
    return await service.get_products(srch_name=search, category_id=category_id)

@router.get('/categories', response_model=List[CategorySchema])
async def get_categories(service: ProductsService = Depends()):
    return await service.get_categories()
