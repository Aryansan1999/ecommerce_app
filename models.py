from pydantic import BaseModel, Field
from typing import List

class SizeItem(BaseModel):
    size: str
    quantity: int

class ProductCreate(BaseModel):
    id: str  # Manually assigned by the user
    name: str
    price: float
    sizes: List[SizeItem]

class ProductOut(BaseModel):
    id: str
    name: str
    price: float

class OrderItem(BaseModel):
    productId: str
    qty: int

class OrderCreate(BaseModel):
    userId: str
    items: List[OrderItem]

class ProductDetails(BaseModel):
    id: str
    name: str

class OrderItemOut(BaseModel):
    productDetails: ProductDetails
    qty: int

class OrderOut(BaseModel):
    id: str
    items: List[OrderItemOut]
    total: float
