
from app.database.conexion import main
def run():
    try:
      main()

    except Exception as e:
        print(f"Hubo un error: {e}")

if __name__ == "__main__":
    run()
