from app.models.user import User
from app.db_connection import get_collection
from bson import ObjectId
from typing import List, Dict, Optional
from fastapi import HTTPException
import hashlib
import os
from typing import Optional

# Password hashing

collection = get_collection("users")  # Specify collection name

def hash_password(password: str) -> str:
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + key.hex()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    salt = bytes.fromhex(hashed_password[:64])
    key = bytes.fromhex(hashed_password[64:])
    new_key = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100000)
    return key == new_key

def create_user(user: User) -> str:
    # Check if username exists
    if collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user.password = hash_password(user.password)
    result = collection.insert_one(user.model_dump(by_alias=True))
    return str(result.inserted_id)

def get_users() -> List[Dict]:
    return list(collection.find({}, {"_id": 0}))

def get_user_by_username(username: str) -> Optional[Dict]:
    return collection.find_one({"username": username}, {"_id": 0})

def authenticate_user(credential: str, password: str) -> Optional[Dict]:
    # Check if credential is email or username
    if '@' in credential:
        user = collection.find_one({"email": credential})
    else:
        user = collection.find_one({"username": credential})
    
    if user and verify_password(password, user["password"]):
        return {k: v for k, v in user.items() if k != "password"}
    return None

def update_user(username: str, update_data: Dict) -> bool:
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
    result = collection.update_one({"username": username}, {"$set": update_data})
    return result.modified_count > 0

def delete_user(username: str) -> bool:
    result = collection.delete_one({"username": username})
    return result.deleted_count > 0