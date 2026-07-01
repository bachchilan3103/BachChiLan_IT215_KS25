from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

products = [
    {
        "id": 1,
        "code": "SP001",
        "name": "Laptop Dell",
        "price": 15000000,
        "stock": 10
    },
    {
        "id": 2,
        "code": "SP002",
        "name": "Mouse Logitech",
        "price": 350000,
        "stock": 50
    }
]

class ProductCreate(BaseModel):
    code: str
    name: str
    price: float
    stock: int

@app.post("/products", status_code=201)
def create_product(product: ProductCreate):
    for p in products:
        if p["code"] == product.code:
            raise HTTPException(
                status_code=400,
                detail=f"Mã sản phẩm '{product.code}' đã tồn tại."
            )
    
    new_id = max(p["id"] for p in products) + 1 if products else 1
    
    new_product = {
        "id": new_id,
        "code": product.code,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }
    products.append(new_product)
    return new_product
