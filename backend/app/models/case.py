from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional

class YearLoss(BaseModel):
    year: int = Field(..., ge=2000, le=2100, description="Tahun pemantauan (2000-2100)")
    tc_loss_ha: float = Field(..., ge=0, description="Luas kehilangan tutupan pohon dalam hektar")

class DriverData(BaseModel):
    driver: str = Field(..., description="Penyebab kerusakan (misal: Perkebunan, Kebakaran)")
    losses: List[YearLoss] = Field(..., min_length=1, description="Daftar data kehilangan per tahun")

class Case(BaseModel):
    # Tambahkan field ID agar kompatibel dengan MongoDB
    id: Optional[str] = Field(None, alias="_id", description="ID unik dari MongoDB")
    country: str = Field(..., description="Nama negara")
    threshold: int = Field(default=30, gt=0, description="Ambang batas persentase tutupan pohon")
    drivers: List[DriverData] = Field(default_factory=list)
    sdg_indicator: str = Field(default="15.2.1", description="Indikator SDG 15 terkait pengelolaan hutan")

    # Konfigurasi Pydantic v2
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        json_schema_extra={
            "example": {
                "country": "Indonesia",
                "threshold": 30,
                "drivers": [
                    {
                        "driver": "Commodity-driven deforestation",
                        "losses": [{"year": 2021, "tc_loss_ha": 1500.5}]
                    }
                ]
            }
        }
    )

    @field_validator('drivers')
    @classmethod
    def validate_no_duplicate_years(cls, drivers: List[DriverData]) -> List[DriverData]:
        for driver_data in drivers:
            years = [loss.year for loss in driver_data.losses]
            # Validasi duplikasi tahun
            if len(years) != len(set(years)):
                raise ValueError(f"Terdapat duplikasi tahun pada driver: {driver_data.driver}")
            # Validasi minimal 1 data loss
            if not years:
                raise ValueError(f"Driver {driver_data.driver} harus memiliki minimal 1 data tahunan")
        return drivers