from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from app.model.models import Product

# Create Product
async def create_product(session: AsyncSession, product_data: dict):
    product = Product(**product_data)  # accept raw dict
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product

# Get all products
async def get_products(session: AsyncSession):
    result = await session.exec(select(Product))
    return result.all()

# Get single product by ID
async def get_product(session: AsyncSession, product_id: int):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Update Product
async def update_product(session: AsyncSession, product_id: int, product_data: dict):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product_data.items():  # use dict directly
        setattr(product, key, value)
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product

# Delete Product
async def delete_product(session: AsyncSession, product_id: int):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await session.delete(product)
    await session.commit()
    return {"detail": "Product deleted"}
