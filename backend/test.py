# main.py
import uvicorn
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.middleware.error_handler import custom_error_handler

# 1. Load Environment Variables
load_dotenv()

# 2. Inisialisasi FastAPI
app = FastAPI(
    title="Global Forest API",
    description="Dashboard Pemantauan Kerusakan Hutan untuk UAS",
    version="1.0.0"
)

# 3. Mendaftarkan Global Error Handler (Pindahkan ke sini agar lebih rapi)
app.add_exception_handler(Exception, custom_error_handler)

# 4. Pengaturan CORS untuk Frontend Vue.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        
    allow_credentials=True,
    allow_methods=["*"],        
    allow_headers=["*"],
)

# 5. Import & Koneksi Database (Memicu eksekusi database.py)
from app.db_connection import forest_collection 

# 6. Routing (Menghubungkan ke folder routes)
# from app.routes.forest import router as forest_router
from app.routes.case_routes import router as case_router
from app.routes.news_routes import router as news_router

app.include_router(case_router, prefix="/api/case", tags=["Case Monitoring"])
app.include_router(news_router, prefix="/api/news", tags=["News"])

@app.get("/")
async def root():
    return {"message": "API SDG 15 Forest Monitoring Aktif"}

# 7. Server Running
if __name__ == "__main__":
    # Mengambil port dari .env, default ke 8000
    port = int(os.getenv("PORT", 8000))
    print(f"Server running on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)