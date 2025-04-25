from sqlalchemy.orm import declarative_base, Mapped, mapped_column



Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    quantity: Mapped[int]

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name={self.name}, description={self.description}, price={self.price}, quantity={self.quantity})>"