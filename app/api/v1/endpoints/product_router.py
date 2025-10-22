from fastapi import APIRouter, Depends, Body
from app.db.session import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.controller import product_controller as controller

router = APIRouter(prefix="/products", tags=["Products"])

# Create Product
@router.post("/", response_model=dict)
async def create_product_route(
    product: dict = Body(...), 
    session: AsyncSession = Depends(get_session)
):
    return await controller.create_product(session, product)

# Get all products
@router.get("/", response_model=list)
async def get_products_route(session: AsyncSession = Depends(get_session)):
    return await controller.get_products(session)

# Get single product by ID
@router.get("/{product_id}", response_model=dict)
async def get_product_route(product_id: int, session: AsyncSession = Depends(get_session)):
    return await controller.get_product(session, product_id)

# Update Product
@router.put("/{product_id}", response_model=dict)
async def update_product_route(
    product_id: int, 
    product: dict = Body(...), 
    session: AsyncSession = Depends(get_session)
):
    return await controller.update_product(session, product_id, product)

# Delete Product
@router.delete("/{product_id}")
async def delete_product_route(product_id: int, session: AsyncSession = Depends(get_session)):
    return await controller.delete_product(session, product_id)
