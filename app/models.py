from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field()
    email: str = Field()
    password: str = Field()
    birthdate: str = Field()

class UserLogin(BaseModel):
    email: str = Field()
    password: str = Field()

class UserResponse(BaseModel):
    name: str = Field()
    email: str = Field()
    birthdate: str = Field()
    
