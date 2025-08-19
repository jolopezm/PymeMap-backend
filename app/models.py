from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field()
    email: str = Field()
    birthdate: str = Field()
    