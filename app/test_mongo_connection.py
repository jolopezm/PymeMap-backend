import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv
 
print("Iniciando prueba de conexión a MongoDB...")
print(f"Ruta de certificados (certifi): {certifi.where()}")

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    print("\nERROR: No se encontró la variable MONGO_URI en el archivo .env")
else:
    try:
        print("Intentando conectar...")
        # Usamos MongoClient (síncrono) para esta prueba simple
        client = MongoClient(
            MONGO_URI,
            tls=True,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=10000 # Timeout de 10 segundos
      )
        # Este comando es una forma simple de verificar la conexión
        client.admin.command('ping')
        print("\n>>> ¡ÉXITO! La conexión con MongoDB se ha establecido correctamente.")
    except Exception as e:
        print("\n>>> FALLO: No se pudo conectar a MongoDB.")
        print(f"   Tipo de Error: {type(e).__name__}")
        print(f"   Detalles: {e}")