# app/database.py
import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Mengambil variabel dari .env
uri = os.getenv("CONNECTION_STRING")
db_name = os.getenv("DB_NAME", "globalforest")

try:
    # Koneksi ke MongoDB Lokal
    client = motor.motor_asyncio.AsyncIOMotorClient(uri)
    database = client[db_name]
    
    # Koleksi untuk data SDG 15
    forest_collection = database["logs_kerusakan"]
    
    print(f"Berhasil terhubung ke MONGODB LOKAL | DB: {db_name}")
except Exception as e:
    print(f"Gagal koneksi ke MongoDB Lokal: {e}")