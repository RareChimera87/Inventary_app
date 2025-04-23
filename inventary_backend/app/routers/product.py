from pydantic import BaseModel, field_validator
from fastapi import APIRouter

router = APIRouter()

class Product(BaseModel):
    name: str
    description: list
    price: float
    quantity: int

    @field_validator("price")
    def validaPrice(value):
        if value < 0:
            raise ValueError(f"El precio debe ser un valor positivo: {value}")
        return value
    
    @field_validator("quantity")
    def validaQuantity(value):
        if value < 0:
            raise ValueError(f"La cantidad debe ser un valor positivo: {value}")
        return value

prueba_producto = {
    'name': 'Pan',
    'description': ["bonito, util"],
    'price': -10,
    'quantity': 1
}


products_db = []

@router.get("/products")
def getProducts():
    return products_db

@router.post("/products")
def postProducts(product: Product):
    products_db.append(product.model_dump())
    return {"message": "Producto creado exitosamente!"}