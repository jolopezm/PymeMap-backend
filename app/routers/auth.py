from fastapi import APIRouter, HTTPException, Depends, status
from datetime import timedelta

from ..db import db
from ..models import UserLogin
from ..auth import (
    create_access_token,
    verify_password,
    Token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(form_data: UserLogin):
    """Autenticates the user and returns an access token"""
    user = await db.users.find_one({"email": form_data.email})
    if not user or not verify_password(form_data.password, user["password"]):
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
