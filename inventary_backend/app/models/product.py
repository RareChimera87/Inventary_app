import sqlalchemy as sa
from sqlalchemy.orm import declarative_base



Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = sa.Column(sa.Integer, primary_key=True)
    name  = sa.Column( sa.String)
    description = sa.Column(sa.String)
    price = sa.Column(sa.Integer)
    quantity = sa.Column( sa.Integer)
