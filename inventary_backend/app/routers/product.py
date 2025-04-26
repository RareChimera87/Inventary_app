from pydantic import BaseModel, field_validator
from fastapi import APIRouter, Depends, HTTPException, status
from app.database.conexion import get_db, Product
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter()

class ProductSearch(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    category: Optional[str] = None
    SKU: Optional[int] = None
    state: Optional[bool] = None
    supplier_id: Optional[int] = None

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
    SKU: int
    minim_stock: int
    state: bool
    category: str
    supplier_id: int

    @field_validator("price")
    def validaPrice(value):
        if value < 0:
            raise ValueError(f"El precio debe ser un valor positivo: {value}")
        return value
    
    @field_validator("SKU")
    def validaSKU(value):
        if value < 0:
            raise ValueError(f"El SKU debe ser un valor positivo: {value}")
        return value
    
    @field_validator("minim_stock")
    def validaMinStock(value):
        if value < 0:
            raise ValueError(f"El Minimo Stock debe ser un valor positivo: {value}")
        return value
    
    @field_validator("quantity")
    def validaQuantity(value):
        if value < 0:
            raise ValueError(f"La cantidad debe ser un valor positivo: {value}")
        return value



@router.get("/products")
def getProducts(db: Session = Depends(get_db)):
    try:
        products = db.query(Product).all()
    except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Hubo un error al : {e}")
    if not products:
        raise  HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No hay productos")
    return products

@router.get("/products/search/")
def searchProduct(filters: ProductSearch = Depends(), db: Session = Depends(get_db)):
    query = db.query(Product)

    if filters.id:
        query = query.filter(Product.id == filters.id)
    if filters.name:
        query = query.filter(Product.name.ilike(f"%{filters.name}%"))
    if filters.category:
        query = query.filter(Product.category == filters.category)
    if filters.SKU:
        query = query.filter(Product.SKU == filters.SKU)
    if filters.state is not None:
        query = query.filter(Product.state == filters.state)
    if filters.supplier_id:
        query = query.filter(Product.supplier_id == filters.supplier_id)

    producto = query.all()
    if producto:
        return producto
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El producto no existe")


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
        try:
            db.delete(producto)
            db.commit()
            return {"message": "Producto eliminado exitosamente", "Producto": producto}
        except Exception as e:
            db.rollback()  # Importante para revertir los cambios si ocurre un error
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Hubo un error al eliminar el producto: {e}")
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El producto no existe")

@router.put("/update/products/{id}")
def updateProduct(id: int, product: ProductCreate, db: Session = Depends(get_db)):
    producto = db.query(Product).filter(Product.id == id).first()
    if producto:
        try:
            producto.name = product.name
            producto.description = product.description
            producto.price = product.price
            producto.quantity = product.quantity
            producto.SKU = product.SKU
            producto.minim_stock = product.minim_stock
            producto.state = product.state
            producto.category = product.quantity
            producto.supplier_id = product.supplier_id
            
            db.commit()
            return {"message": "Producto actualizado exitosamente", "Producto": producto}
        
        except Exception as e:
            db.rollback() 
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Hubo un error al eliminar el producto: {e}")
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El producto no existe")