from fastapi import FastAPI
from models import Product
from database import SessionLocal


app = FastAPI()


product_list = [
Product(id=10, name="Laptop", description="2026 Laptop", price=33.00, quantity=10),
Product(id=11, name="Keyboard", description="Mechanical Keyboard", price=15.00, quantity=25),
Product(id=12, name="Mouse", description="Wireless Mouse", price=10.00, quantity=30),
Product(id=13, name="Monitor", description="24-inch LED Monitor", price=120.00, quantity=15),
Product(id=14, name="Printer", description="All-in-One Inkjet Printer", price=80.00, quantity=8),
Product(id=15, name="Scanner", description="Flatbed Document Scanner", price=60.00, quantity=10),
]




@app.get("/")
def greet ():
    return "Welcome to fast api"


@app.get("/products")
def get_all_products():
    return product_list

@app.get("/product/{id}")
def get_product(id:int):
    for product in product_list:
        if product.id == id:
            return product
    return "No Product Found"

@app.post("/product")
def add_product(product:Product):
    product_list.append(product)
    return product_list


@app.put("/product/{id}")
def update_product(id:int, product:Product):
    for i in range(len(product_list)):
        if product_list[i].id == id:
            print("product",product)
            product_list[i] = product
            return product_list[i]
        
    return "Product Not Found"


@app.delete("/product/{id}")
def update_product(id:int):
    for i in range(len(product_list)):
        if product_list[i].id == id:
            product_list.remove(product_list[i])
            return product_list
        
    return "Product Not Found"