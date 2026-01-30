import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pandas as pd

# from connection.db_connection import get_collection
from app.db_connection import get_collection
from app.models.case import Case, YearLoss, DriverData
from typing import Dict

collection = get_collection()

def extract_and_insert(excel_file: str):
    # Read Excel dengan pandas
    df = pd.read_excel(excel_file, sheet_name="Country drivers", engine="openpyxl")
    
    # Group by country dan driver untuk struktur nested
    grouped = df.groupby(["country", "driver"])
    
    inserted_count = 0
    for (country, driver), group in grouped:
        # Cari existing document untuk country (upsert jika perlu)
        existing = collection.find_one({"country": country})
        if not existing:
            case = Case(country=country, drivers=[])
            collection.insert_one(case.model_dump())
            existing_id = collection.find_one({"country": country})["_id"]
        else:
            existing_id = existing["_id"]
        
        # Buat DriverData
        losses = [YearLoss(year=row["year"], tc_loss_ha=row["tc_loss_ha"]) for _, row in group.iterrows()]
        driver_data = DriverData(driver=driver, losses=losses)
        
        # Update nested drivers
        collection.update_one(
            {"_id": existing_id},
            {"$push": {"drivers": driver_data.model_dump()}}
        )
        inserted_count += 1
    
    print(f"Inserted/Updated {inserted_count} driver groups.")

# Jalankan script
if __name__ == "__main__":
    extract_and_insert("global_05212025.xlsx")  # Ganti path jika perlu