from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class User(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    username: str = Field(..., min_length=3, max_length=50)
    password: str  # In production, this should be hashed
    email: Optional[str] = None
    role: str = Field(default="user")  # e.g., "user", "admin"

    class Config:
        validate_by_name = True
        json_encoders = {ObjectId: str}

class LoginRequest(BaseModel):
    credential: str
    password: str