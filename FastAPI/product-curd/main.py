from fastapi import FastAPI, Depends
from models import Product
from database import session,engine
import database_models
from sqlalchemy.orm import Session


app = FastAPI()

database_models.Base.metadata.create_all(bind=engine) # create table into db


# product_list = [
# Product(id=10, name="Laptop", description="2026 Laptop", price=33.00, quantity=10),
# Product(id=11, name="Keyboard", description="Mechanical Keyboard", price=15.00, quantity=25),
# Product(id=12, name="Mouse", description="Wireless Mouse", price=10.00, quantity=30),
# Product(id=13, name="Monitor", description="24-inch LED Monitor", price=120.00, quantity=15),
# Product(id=14, name="Printer", description="All-in-One Inkjet Printer", price=80.00, quantity=8),
# Product(id=15, name="Scanner", description="Flatbed Document Scanner", price=60.00, quantity=10),
# ]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = session()
    count= db.query(database_models.Product).count()    
    if count == 0:
        for product in product_list:
            db.add(database_models.Product(**product.model_dump()))

    db.commit()


init_db()

@app.get("/")
def greet ():
    return "Welcome to fast api"


@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/product/{id}")
def get_product(id:int,db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product


    return "No Product Found"

# Need to fixed post issue
@app.post("/product")
def add_product(product:Product,db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    #db.add(database_models.Product(**product.dict()))
    db.commit()
   
    return {
        "message": "Product added successfully",
        "product": product
    }


@app.put("/product/{id}")
def update_product(id:int, product:Product,db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product Updated Successfully"


@app.delete("/product/{id}")
def update_product(id:int,db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return "Product delete successfully"