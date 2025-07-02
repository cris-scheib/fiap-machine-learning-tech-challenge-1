from pydantic import BaseModel

class BookSchema(BaseModel):
    id: int
    title: str
    price: float
    availability: str
    rating: int
    category: str

    class Config:
        from_attributes = True