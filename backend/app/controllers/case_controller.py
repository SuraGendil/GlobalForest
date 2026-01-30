from app.models.case import Case, YearLoss, DriverData
from app.db_connection import get_collection
from bson import ObjectId
from typing import List, Dict, Optional
from fastapi import HTTPException

collection = get_collection()

def create_or_append_case(country: str, driver: str, losses: List[Dict], threshold: Optional[int] = None) -> str:
    if not losses:
        raise HTTPException(status_code=422, detail="At least 1 loss entry required")

    # Konversi ke YearLoss, validasi min 1
    loss_objects = [YearLoss(**loss) for loss in losses]

    # Cari existing
    existing = collection.find_one({"country": country})
    if not existing:
        new_driver = DriverData(driver=driver, losses=loss_objects)
        new_case = Case(country=country, drivers=[new_driver], threshold=threshold if threshold is not None else 30)
        result = collection.insert_one(new_case.model_dump())
        return str(result.inserted_id)

    # Check driver
    driver_index = next((i for i, d in enumerate(existing['drivers']) if d['driver'] == driver), None)
    if driver_index is None:
        new_driver = DriverData(driver=driver, losses=loss_objects).model_dump()
        collection.update_one({"_id": existing['_id']}, {"$push": {"drivers": new_driver}})
        if threshold is not None:
            collection.update_one({"_id": existing['_id']}, {"$set": {"threshold": threshold}})
        return str(existing['_id'])

    # Handle duplicate years (Update instead of Conflict)
    existing_years_indices = {loss['year']: idx for idx, loss in enumerate(existing['drivers'][driver_index]['losses'])}
    
    losses_to_push = []
    
    for loss in loss_objects:
        if loss.year in existing_years_indices:
            # Update existing year data
            idx = existing_years_indices[loss.year]
            collection.update_one(
                {"_id": existing['_id']},
                {"$set": {f"drivers.{driver_index}.losses.{idx}.tc_loss_ha": loss.tc_loss_ha}}
            )
        else:
            losses_to_push.append(loss)

    if losses_to_push:
        collection.update_one(
            {"_id": existing['_id'], "drivers.driver": driver},
            {"$push": {"drivers.$.losses": {"$each": [l.model_dump() for l in losses_to_push]}}}
        )
        
    if threshold is not None:
        collection.update_one({"_id": existing['_id']}, {"$set": {"threshold": threshold}})
        
    return str(existing['_id'])

def create_case(case: Case) -> str:
    # Check duplikat di level model
    return str(collection.insert_one(case.model_dump()).inserted_id)

def read_cases(country: Optional[str] = None, driver: Optional[str] = None, year: Optional[int] = None, page: int = 1, limit: int = 10) -> Dict:
    query = {}
    if country: query["country"] = {"$regex": country, "$options": "i"}
    if driver: query["drivers.driver"] = {"$regex": driver, "$options": "i"}
    if year: query["drivers.losses.year"] = year

    print(f"Query: {query}, year: {year}, type: {type(year)}")

    # Pipeline for total count
    total_pipeline = [
        {"$match": query},
        {"$unwind": "$drivers"},
        {"$unwind": "$drivers.losses"},
        {"$count": "total"}
    ]
    total_result = list(collection.aggregate(total_pipeline))
    total = total_result[0]["total"] if total_result else 0

    # Pipeline for data
    data_pipeline = [
        {"$match": query},
        {"$unwind": "$drivers"},
        {"$unwind": "$drivers.losses"},
        {"$sort": {"drivers.losses.year": 1}},
        {"$skip": (page - 1) * limit},
        {"$limit": limit},
        {"$project": {
            "_id": 0,
            "id": {"$toString": "$_id"},
            "country": 1,
            "driver": "$drivers.driver",
            "year": "$drivers.losses.year",
            "tc_loss_ha": "$drivers.losses.tc_loss_ha",
            "threshold": 1,
            "sdg_indicator": 1
        }}
    ]
    data = list(collection.aggregate(data_pipeline))

    return {"data": data, "total": total, "page": page, "limit": limit}

def update_case(country: str, driver: str, year: int, new_data: Dict) -> bool:
    if not new_data:
        raise HTTPException(status_code=400, detail="No data to update")

    new_country = new_data.get('country', country)
    new_driver = new_data.get('driver', driver)
    
    # Ensure year is treated as int for comparison
    try:
        new_year = int(new_data.get('year', year))
        current_year = int(year)
    except (ValueError, TypeError):
        new_year = new_data.get('year', year)
        current_year = year
        
    new_loss = new_data.get('tc_loss_ha')
    new_threshold = new_data.get('threshold')

    # Jika kunci (Country, Driver, Year) berubah, lakukan pemindahan data
    if new_country != country or new_driver != driver or new_year != current_year:
        conflict = collection.find_one({
            "country": new_country,
            "drivers": {"$elemMatch": {"driver": new_driver, "losses.year": new_year}}
        })
        if conflict:
            raise HTTPException(status_code=409, detail=f"Data already exists for {new_country}/{new_driver}/{new_year}")

        if not delete_case(country, driver, year):
            raise HTTPException(status_code=404, detail="Original data not found")
        
        loss_val = new_loss if new_loss is not None else 0
        create_or_append_case(new_country, new_driver, [{"year": new_year, "tc_loss_ha": loss_val}])
        
        if new_threshold is not None:
            collection.update_one({"country": new_country}, {"$set": {"threshold": new_threshold}})
            
        return True

    # Check existence
    existing = collection.find_one({
        "country": country,
        "drivers": {"$elemMatch": {"driver": driver, "losses.year": year}}
    })
    if not existing:
        raise HTTPException(status_code=404, detail=f"Data not found for {country}/{driver}/{year}")

    # Update specific loss
    driver_index = next(i for i, d in enumerate(existing['drivers']) if d['driver'] == driver)
    loss_index = next(i for i, l in enumerate(existing['drivers'][driver_index]['losses']) if l['year'] == year)

    update_path = f"drivers.{driver_index}.losses.{loss_index}"
    
    update_fields = {}
    if new_loss is not None:
        update_fields[f"{update_path}.tc_loss_ha"] = new_loss
    if new_threshold is not None:
        update_fields["threshold"] = new_threshold
        
    if not update_fields:
        return False
        
    result = collection.update_one({"_id": existing['_id']}, {"$set": update_fields})
    return result.modified_count > 0

def delete_case(country: str, driver: Optional[str] = None, year: Optional[int] = None) -> bool:
    if not driver:
        # Delete entire country
        result = collection.delete_one({"country": country})
        return result.deleted_count > 0

    if not year:
        # Delete entire driver
        result = collection.update_one({"country": country}, {"$pull": {"drivers": {"driver": driver}}})
        return result.modified_count > 0

    # Delete specific year
    result = collection.update_one(
        {"country": country, "drivers.driver": driver},
        {"$pull": {"drivers.$.losses": {"year": year}}}
    )
    return result.modified_count > 0

def get_dashboard_statistics() -> Dict:
    """
    Melakukan agregasi kompleks menggunakan $facet untuk mendapatkan
    statistik dashboard dalam satu query database yang efisien.
    """
    pipeline = [
        {"$unwind": "$drivers"},
        {"$unwind": "$drivers.losses"},
        
        {"$facet": {
            "top_countries": [
                {"$group": {"_id": "$country", "total_loss": {"$sum": "$drivers.losses.tc_loss_ha"}}},
                {"$sort": {"total_loss": -1}},
                {"$limit": 5},
                {"$project": {"country": "$_id", "total_loss": 1, "_id": 0}}
            ],
            "drivers_breakdown": [
                {"$group": {"_id": "$drivers.driver", "total_loss": {"$sum": "$drivers.losses.tc_loss_ha"}}},
                {"$sort": {"total_loss": -1}},
                {"$project": {"driver": "$_id", "total_loss": 1, "_id": 0}}
            ],
            "yearly_trend": [
                {"$group": {"_id": "$drivers.losses.year", "total_loss": {"$sum": "$drivers.losses.tc_loss_ha"}}},
                {"$sort": {"_id": 1}},
                {"$project": {"year": "$_id", "total_loss": 1, "_id": 0}}
            ]
        }}
    ]
    
    result = list(collection.aggregate(pipeline))
    return result[0] if result else {}