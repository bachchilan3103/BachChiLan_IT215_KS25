from fastapi import FastAPI, Query, HTTPException

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "price": 15000000},
    {"id": 2, "name": "Mouse", "price": 200000},
    {"id": 3, "name": "Keyboard", "price": 500000},
    {"id": 4, "name": "Monitor", "price": 3000000}
]

@app.get("/products")
def get_products(keyword: str = Query(None), max_price: float = Query(None)):
    if max_price is not None and max_price < 0:
        raise HTTPException(status_code=400, detail="max_price không được âm")

    result = products

    if keyword:
        result = [p for p in result if keyword.lower() in p["name"].lower()]

    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]

    return result
