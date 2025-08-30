from fastapi import APIRouter, HTTPException, Depends, status
from bson import ObjectId

from ..db import db
from ..models import User, UserResponse
from ..auth import get_current_user, get_password_hash, TokenData

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
async def get_users(current_user: TokenData = Depends(get_current_user)):
    """Obtiene todos los usuarios - Ruta protegida que requiere autenticación"""
    users = []
    cursor = db.users.find({}, {"password": 0})
    async for document in cursor:
        users.append(UserResponse(**document))
    return users

@router.post("/", response_model=UserResponse)
async def create_user(user: User):
    """Crea un nuevo usuario con contraseña hasheada"""
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
        
    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user.password)
    
    await db.users.insert_one(user_dict)
    # Return the created user by finding it again, as insert_one doesn't return the full document
    created_user = await db.users.find_one({"email": user.email})
    return UserResponse(**created_user)

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: TokenData = Depends(get_current_user)):
    """Obtener información del usuario actual"""
    user = await db.users.find_one({"email": current_user.email}, {"password": 0})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse(**user)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, current_user: TokenData = Depends(get_current_user)):
    """Obtiene un usuario por su ID - Ruta protegida"""
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    user = await db.users.find_one({"_id": ObjectId(user_id)}, {"password": 0})
    if user:
        return UserResponse(**user)
    raise HTTPException(status_code=404, detail="User not found")
