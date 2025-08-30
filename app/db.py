import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de .env

MONGO_URI = os.getenv("MONGO_URI")

# Configuración mejorada para SSL en Windows
client = AsyncIOMotorClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where(),  # Usa los certificados de certifi
    serverSelectionTimeoutMS=5000  # Reducir timeout para diagnóstico más rápido
)

db = client['myDatabase']  # O db = client['myDatabase']
