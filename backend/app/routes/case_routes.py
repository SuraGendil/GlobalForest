from fastapi import APIRouter, Body, HTTPException, Query
# from controllers.case_controller import create_or_append_case, read_cases, update_case, delete_case
from app.controllers.case_controller import create_or_append_case, read_cases, update_case, delete_case
from typing import List, Dict, Optional

router = APIRouter()

@router.post("/cases")
def create(
    country: str = Body(...),
    driver: str = Body(...),
    losses: List[Dict] = Body(...)  # Format: [{"year": 2021, "tc_loss_ha": 999}, {"year": 2022, "tc_loss_ha": 333}]
):
    try:
        id = create_or_append_case(country, driver, losses)
        return {"id": id, "message": "Case created or appended"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/cases", response_model=Dict)
def read(
    country: Optional[str] = Query(None),
    driver: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100)
):
    return read_cases(country, driver, year, page, limit)

@router.put("/cases", openapi_extra={"examples": {"example": {"value": {"country": "Anomali2", "driver": "Sawit", "year": 2021, "new_data": {"tc_loss_ha": 1000}}}}}
)
def update(
    country: str = Body(...),
    driver: str = Body(...),
    year: int = Body(..., ge=2000),
    new_data: Dict = Body(...)
):
    if update_case(country, driver, year, new_data):
        return {"message": "Case updated"}
    raise HTTPException(status_code=404, detail="Case not found")

@router.delete("/cases")
def delete(
    country: str = Query(...),
    driver: Optional[str] = Query(None),
    year: Optional[int] = Query(None)
):
    if delete_case(country, driver, year):
        return {"message": "Deletion successful"}
    raise HTTPException(status_code=404, detail="No data found to delete")