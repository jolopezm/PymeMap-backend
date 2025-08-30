from fastapi import APIRouter, HTTPException, Depends, status
from ..db import db
from ..models import Business

router = APIRouter()

@router.get("/", response_model=list[Business])
async def get_business():
    business = []
    cursor = db.business.find({})
    async for document in cursor:
        business.append(Business(**document))
    return business

@router.post("/", response_model=Business)
async def create_business(business: Business):
    """Crea un nuevo negocio"""
    existing_business = await db.business.find_one({"name": business.name})
    if existing_business:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name already registered"
        )
        
    business_dict = business.dict()
    
    await db.business.insert_one(business_dict)
    created_business = await db.business.find_one({"name": business.name})
    return Business(**created_business)
