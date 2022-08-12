from fastapi import APIRouter   

from .products import router as products_router
from .orders import router as orders_router

router = APIRouter()
router.include_router(products_router)
router.include_router(orders_router)