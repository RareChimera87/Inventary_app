## IMPORTAR DEPENDENCIAS Y MODULOS

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column, relationship
from dotenv import load_dotenv
import os
import pytz
from datetime import datetime

## CARGAR VARIABLES DE ENTORNO
load_dotenv()


DBDVR = os.getenv("DBDVR")
USER = os.getenv("USER")
PASS = os.getenv("PASS")
HOST = os.getenv("HOSTNAME")
PORT = os.getenv("DBPORT")
DB = os.getenv("DB")


## DEFINIR URL DB
url_db = DBDVR + "://" + USER + ":" + PASS + "@" + HOST + ":" + PORT + "/" + DB

engine = sa.create_engine(url_db)
Session = sessionmaker(bind=engine)
Base = declarative_base()
colombia_tz = pytz.timezone('America/Bogota')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

##DEFINIR MODELOS

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    quantity: Mapped[int]

    supplier_id: Mapped[int] = mapped_column(sa.ForeignKey("suppliers.id"))

    supplier: Mapped["Supplier"] = relationship("Suppliers", back_populates="products")

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name={self.name}, description={self.description}, price={self.price}, quantity={self.quantity})>"
    

class Suppliers(Base):
    __tablename__ = "suppliers"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    address: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    preferred_payment_method: Mapped[str] = mapped_column(sa.String(50))
    created_at: Mapped[sa.TIMESTAMP] = mapped_column(sa.TIMESTAMP, default=datetime.now(colombia_tz))

    products: Mapped[list["Product"]] = relationship("Product", back_populates="supplier")





## FUNCION PRINCIPAL

def main() -> None:
    Base.metadata.create_all(engine)
    
    supplier = Suppliers(name="Proveedor A", address="Dirección A", phone="123456789", email="proveedor@a.com", preferred_payment_method="NEQUI")

    product = Product(name="Producto A", description="Descripción del producto A", price=100, quantity=50, supplier_id=supplier.id)

    product.supplier = supplier
    


    with Session() as session:
        session.add(supplier)
        session.commit()

        session.add(product)
        session.commit()

        product_from_db = session.query(Product).first()
        print(product_from_db.supplier.name)  # Esto imprimirá el nombre del proveedor asociado 


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()