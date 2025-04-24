import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from app.models.product import Product

Base = declarative_base()

url_db = sa.URL.create(
    "postgresql+psycopg2",
    username="postgres",
    password="Cata2013", 
    host="localhost",
    database="inventary_app",
)

engine = sa.create_engine(url_db)

# Conexión opcional (si necesitas una conexión directa en algún momento)
def get_connection():
    return engine.connect()

def close_connection(connection):
    connection.close()  # Cierra la conexión cuando ya no la necesites
