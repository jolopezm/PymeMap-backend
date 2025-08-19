from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta
from app.db import db
from app.models import User, UserLogin, UserResponse
from app.auth import (
    get_password_hash,
    create_access_token,
    verify_password,
    get_current_user,
    Token,
    ACCESS_TOKEN_EXPIRE_MINUTES
    )


router = APIRouter()

@router.get("/users")
async def get_users(current_user: UserResponse = Depends(get_current_user)):
    """Obtiene todos los usuarios - Ruta protegida que requiere autenticación"""
    users = []
    cursor = db.users.find({}, password=0) # excluye las contraseñas para no devolverlas
    async for document in cursor:
        document["_id"] = str(document["_id"])
        users.append(document)
    return users

@router.post("/users")
async def create_user(user: User):
    """Crea un nuevo usuario con contraseña hasheada"""
    # verifica si el usuario ya existe
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
        
    # heshea la contraseña antes de guardar
    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user.password)
    
    result = await db.users.insert_one(user.dict())
    return {"inserted_id": str(result.inserted_id), "message": "User created successfully"}

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    """Autentica al usuario y devuelve un token de acceso"""
    user = await db.users.find_one({"email": user.email})
    if not user or not verify_password(user.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"], "name": user["name"]}, 
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """Obtener información del usuario actual"""
    user = await db.users.find_one({"email": current_user.email}, {"password": 0})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse(**user)