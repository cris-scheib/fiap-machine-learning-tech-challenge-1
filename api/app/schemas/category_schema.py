from pydantic import BaseModel

class CategorySchema(BaseModel):
    category: str

    class Config:
        # from_attributes = True
        orm_mode = True