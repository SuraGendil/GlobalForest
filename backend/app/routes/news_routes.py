from fastapi import APIRouter, HTTPException
from app.controllers.news_controller import get_all_news

router = APIRouter()

@router.get("/news")
async def read_news():
    try:
        news = get_all_news()
        return {"data": news}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))