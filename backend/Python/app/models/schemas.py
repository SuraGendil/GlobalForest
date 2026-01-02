# app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 1. Skema Dasar (Base Schema)
class ForestLogBase(BaseModel):
    country: str = Field(..., description="Negara lokasi kerusakan hutan")
    driver: str = Field(..., description="Penyebab utama (misal: Fire, Logging)")
    year: int = Field(..., gt=1900, description="Tahun kejadian")
    loss: float = Field(..., gt=0, description="Luas hutan yang hilang (Hektar)")

# 2. Skema untuk Input Data (Create)
class ForestLogCreate(ForestLogBase):
    pass

# 3. Skema untuk Respon API (Output)
class ForestLogResponse(ForestLogBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True