from typing import List
from fastapi import APIRouter, Depends

from ..services.orders import OrdersService
from ..schemas.orders import OrdersResponseSchema, UpdateOrderStatusSchema

router = APIRouter(
    prefix='/orders',
    tags=['Orders'],
)

@router.get('/', response_model=OrdersResponseSchema)
async def get_orders(status: str = "", 
    desc: int = 1, # sorting, 0 - asc, 1 - desc
    search_user_name: str = "", 
    user_id: int = 0,
    service: OrdersService = Depends()
    ):
    return await service.get_orders(status, desc, search_user_name, user_id)

@router.patch('/update')
async def update_status(data: UpdateOrderStatusSchema, service: OrdersService = Depends()):
    return await service.update_status(data)

@router.get("/excel/{filename:str}")
async def make_excel_file(filename: str, 
    user_id: int = 0,
    status: str = "",
    desc: int = 1, # sorting, 0 - asc, 1 - desc
    search_user_name: str = "",
    service: OrdersService = Depends()):
    return await service.make_excel_file(filename=filename, user_id=user_id, status=status, desc=desc, search=search_user_name)
