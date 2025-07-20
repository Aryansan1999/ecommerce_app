from fastapi import APIRouter, HTTPException
from models import ProductCreate, ProductOut
from database import db

router = APIRouter()

@router.post("/products", status_code=201)
async def create_product(product: ProductCreate):
    product_dict = product.dict()
    await db.products.insert_one(product_dict)
    return {"id": product_dict["id"]}

@router.get("/products", response_model=list[ProductOut])
async def list_products():
    cursor = db.products.find()
    products = []
    async for product in cursor:
        products.append(ProductOut(id=product["id"], name=product["name"], price=product["price"]))
    return products

@router.get("/products/{product_id}", response_model=ProductOut)
async def get_product(product_id: str):
    product = await db.products.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductOut(id=product["id"], name=product["name"], price=product["price"])
