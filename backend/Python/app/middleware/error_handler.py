# app/middleware/error_handler.py
from fastapi import Request
from fastapi.responses import JSONResponse
from app.constants import StatusCodes
import traceback
import os

async def custom_error_handler(request: Request, exc: Exception):
    # Mengambil status code. Jika HTTPException, ambil status_code-nya. 
    status_code = getattr(exc, "status_code", 500)
    
    error_title = "Unknown Error"
    
    # Logika switch-case menggunakan if-elif
    if status_code == StatusCodes.VALIDATION_ERROR:
        error_title = "Validation Error"
    elif status_code == StatusCodes.UNAUTHORIZED:
        error_title = "Unauthorized"
    elif status_code == StatusCodes.FORBIDDEN:
        error_title = "Forbidden"
    elif status_code == StatusCodes.NOT_FOUND:
        error_title = "Not Found"
    elif status_code == StatusCodes.SERVER_ERROR:
        error_title = "Server Error"

    # Menyiapkan respon JSON mirip dengan struktur Express Anda
    response_content = {
        "title": error_title,
        "message": str(exc),
    }

    # Tambahkan stackTrace hanya jika dalam mode development
    if os.getenv("DEBUG") == "True":
        response_content["stackTrace"] = traceback.format_exc()

    return JSONResponse(
        status_code=status_code,
        content=response_content
    )