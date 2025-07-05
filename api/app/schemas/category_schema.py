from pydantic import BaseModel

class CategorySchema(BaseModel):
    name: str