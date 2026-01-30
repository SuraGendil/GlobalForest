from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.case_routes import router as case_router
from app.routes.user_routes import router as user_router
from app.routes.news_routes import router as news_router
from app.middleware.error_handler import error_handler
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.include_router(case_router, prefix="/api/case", tags=["Case Monitoring"])
app.include_router(user_router, prefix="/api/user", tags=["User Management"])
app.include_router(news_router, prefix="/api/news", tags=["News"])
app.add_exception_handler(Exception, error_handler)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)