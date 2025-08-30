from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler=None):
        return {'type': 'string'}

class User(BaseModel):
    rut: str = Field()
    name: str = Field()
    email: str = Field()
    password: str = Field()
    birthdate: str = Field()

class UserLogin(BaseModel):
    email: str = Field()
    password: str = Field()

class UserResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    rut: str = Field(...)
    name: str = Field(...)
    email: str = Field(...)
    birthdate: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        
class Business(BaseModel):
    name: str = Field(...)
    address: str = Field(...)
    category: str = Field(...)
    description: str = Field(...)
    #owner_id: PyObjectId = Field(default_factory=PyObjectId)
    owner_id: str = Field(...)