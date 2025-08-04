from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
