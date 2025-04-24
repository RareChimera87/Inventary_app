from app.models.product import Product  # Importa tus modelos
from app.database.conexion import engine, Base, get_connection, close_connection  # Importa el engine y Base

def run():
    try:
        # Crear tablas si no existen
        Base.metadata.create_all(engine)
        print("Las tablas se han creado correctamente.")
        
        # Obtener la conexión
        connection = get_connection()
        
        # Cerrar la conexión
        close_connection(connection)

    except Exception as e:
        print(f"Hubo un error: {e}")

if __name__ == "__main__":
    run()
