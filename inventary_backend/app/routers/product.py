from pydantic import BaseModel, field_validator
from fastapi import APIRouter, Depends, HTTPException, status
from app.database.conexion import get_db, Product
from sqlalchemy.orm import Session

router = APIRouter()



class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
    supplier_id: int

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



@router.get("/products")
def getProducts(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@router.post("/products")
def postProducts(product_data: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(**product_data.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Producto creado exitosamente", "product_id": new_product.id}

@router.delete("/delete/products/{id}")
def deleteProduct(id: int, db: Session = Depends(get_db)):
    producto = db.query(Product).filter(Product.id == id).first()
    if producto:
        db.delete(producto)
        db.commit()
        return {"message": "Producto eliminado exitosamente", "Producto": producto}
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El producto no existe")
    
@router.put("/update/products/{id}")
def updateProduct(id: int, product: ProductCreate, db: Session = Depends(get_db)):
    producto = db.query(Product).filter(Product.id == id).first()
    if producto:
        producto.name = product.name
        producto.description = product.description
        producto.price = product.price
        producto.quantity = product.quantity
        producto.supplier_id = product.supplier_id
        
        
        db.commit()
        return {"message": "Producto actualizado exitosamente", "Producto": producto}
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El producto no existe")