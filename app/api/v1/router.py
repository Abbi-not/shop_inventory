# app/api/v1/endpoints/router.py
from fastapi import APIRouter
from app.api.v1.endpoints.product_router import router as product_router

router = APIRouter()
router.include_router(product_router,  prefix="/product", tags=["product"])
