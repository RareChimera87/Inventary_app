import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, sessionmaker
from app.models.product import Product
from dotenv import load_dotenv
import os

load_dotenv()

DBDVR = os.getenv("DBDVR")
USER = os.getenv("USER")
PASS = os.getenv("PASS")
HOST = os.getenv("HOSTNAME")
PORT = os.getenv("DBPORT")
DB = os.getenv("DB")


url_db = DBDVR + "://" + USER + ":" + PASS + "@" + HOST + ":" + PORT + "/" + DB

engine = sa.create_engine(url_db)
Session = sessionmaker(bind=engine)
Base = declarative_base()




def main() -> None:
    Base.metadata.create_all(engine)
    producto = Product(name="pruebas3", description="mas prueba2", price=102, quantity=1002)

    with Session() as session:
        session.add(producto)

        session.commit()
        print("Producto insertado")

        print(session.query(Product).all())
        print("Consulta:", session.query(Product).all())


