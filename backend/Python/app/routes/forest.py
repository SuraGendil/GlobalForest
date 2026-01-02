from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.schemas import ForestLogCreate, ForestLogResponse 
from app.controllers import forest_controller

router = APIRouter()

# 1. Get All Cases (Read)
@router.get("/", response_model=List[ForestLogResponse])
async def read_forest_logs():
    return await forest_controller.get_cases()

# 2. Create Case (Create)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ForestLogResponse)
async def add_forest_log(log: ForestLogCreate):
    return await forest_controller.create_case(log)

# 3. Get Single Case by ID (Read)
@router.get("/{id}", response_model=ForestLogResponse)
async def read_forest_log(id: str):
    return await forest_controller.get_case(id)

# 4. Update Case (Update)
@router.put("/{id}", response_model=ForestLogResponse)
async def update_forest_log(id: str, log: ForestLogCreate):
    # Mengonversi skema pydantic ke dictionary untuk update
    update_data = log.model_dump() 
    return await forest_controller.update_case(id, update_data)

# 5. Delete Case (Delete)
@router.delete("/{id}")
async def delete_forest_log(id: str):
    return await forest_controller.delete_case(id)

# 6. endpoint summary statistics
@router.get("/stats/summary")
async def read_forest_stats():
    return await forest_controller.get_forest_stats()