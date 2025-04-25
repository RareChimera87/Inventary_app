import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column

url_db = sa.URL.create(
    "postgresql+psycopg2",
    username="postgres",
    password="Cata2013", 
    host="localhost",
    database="inventary_app",
)

engine = sa.create_engine("postgresql://postgres:Cata2013@localhost:5432/inventary_app")
print(engine)
Session = sessionmaker(bind=engine)
Base = declarative_base()



class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    quantity: Mapped[int]

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name={self.name}, description={self.description}, price={self.price}, quantity={self.quantity})>"



def main() -> None:
    Base.metadata.create_all(engine)
    producto = Product(id=0, name="pruebas", description="mas prueba", price=10, quantity=100)

    with Session() as session:
        session.add(producto)

        session.commit()
        print("Producto insertado")

        print(session.query(Product).all())
        print("Consulta:", session.query(Product).all())

if __name__ == "__main__":
    main()
