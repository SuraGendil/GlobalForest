from fastapi import APIRouter, Body, HTTPException, Depends
from app.controllers.user_controller import create_user, get_users, get_user_by_username, authenticate_user, update_user, delete_user
from app.models.user import User, LoginRequest
from typing import List, Dict

router = APIRouter()

@router.post("/users")
def create(user: User):
    try:
        user_id = create_user(user)
        return {"id": user_id, "message": "User created"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users", response_model=List[Dict])
def read():
    return get_users()

@router.get("/users/{username}")
def read_user(username: str):
    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/login")
def login(request: LoginRequest):
    user = authenticate_user(request.credential, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user": user}

@router.put("/users/{username}")
def update(username: str, update_data: Dict = Body(...)):
    if update_user(username, update_data):
        return {"message": "User updated"}
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/users/{username}")
def delete(username: str):
    if delete_user(username):
        return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")