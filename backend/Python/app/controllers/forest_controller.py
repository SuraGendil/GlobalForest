# app/controllers/forest_controller.py
from fastapi import HTTPException, status
from bson import ObjectId
from app.database import forest_collection
from app.models.schemas import ForestLogCreate 
from datetime import datetime

# Helper untuk mengonversi data MongoDB ke dictionary Python
def forest_helper(forest) -> dict:
    return {
        "id": str(forest["_id"]),
        "country": forest["country"],
        "driver": forest["driver"],
        "year": forest["year"],
        "loss": forest["loss"],
        "created_at": forest.get("created_at"),
        "updated_at": forest.get("updated_at"),
    }

# 1. Get All Cases (Read)
async def get_cases():
    forests = []
    async for forest in forest_collection.find():
        forests.append(forest_helper(forest))
    return forests

# 2. Create New Case (Create)
async def create_case(data: ForestLogCreate):
    # Validasi required fields sudah otomatis ditangani Pydantic
    new_forest = data.model_dump() # Mengubah pydantic ke dict
    new_forest["created_at"] = datetime.now()
    new_forest["updated_at"] = datetime.now()
    
    result = await forest_collection.insert_one(new_forest)
    created_forest = await forest_collection.find_one({"_id": result.inserted_id})
    return forest_helper(created_forest)

# 3. Get Single Case (Read)
async def get_case(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID tidak valid")
        
    forest = await forest_collection.find_one({"_id": ObjectId(id)})
    if not forest:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")
    return forest_helper(forest)

# 4. Update Case (Update)
async def update_case(id: str, data: dict):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID tidak valid")
    
    data["updated_at"] = datetime.now()
    updated_forest = await forest_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": data},
        return_document=True
    )
    if not updated_forest:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")
    return forest_helper(updated_forest)

# 5. Delete Case (Delete)
async def delete_case(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID tidak valid")
        
    delete_result = await forest_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": f"Data dengan ID {id} berhasil dihapus"}
    
    raise HTTPException(status_code=404, detail="Data tidak ditemukan")

# 6. Get Forest Statistics (Summary)
async def get_forest_stats():
    pipeline = [
        {
            "$group": {
                "_id": "$country",
                "total_loss": {"$sum": "$loss"},
                "count": {"$sum": 1}
            }
        }
    ]
    cursor = forest_collection.aggregate(pipeline)
    return await cursor.to_list(length=100)