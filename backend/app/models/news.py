from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from bson import ObjectId

class News(BaseModel):
    id: Optional[str] = Field(None, alias="_id", description="ID unik dari MongoDB")
    title: str = Field(..., min_length=3, description="Judul berita")
    summary: str = Field(..., description="Ringkasan berita")
    date: str = Field(..., description="Tanggal publikasi (format string untuk tampilan)")
    link: str = Field(..., description="Link ke sumber berita")
    created_at: datetime = Field(default_factory=datetime.now, description="Waktu data ditambahkan")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "title": "Krisis Deforestasi Global Meningkat",
                "summary": "Laporan terbaru menunjukkan deforestasi di Amazon mencapai rekor tertinggi tahun ini.",
                "date": "6 Januari 2026",
                "link": "https://www.mongabay.co.id/hutan/",
                "created_at": "2026-01-06T12:00:00"
            }
        }
    )
