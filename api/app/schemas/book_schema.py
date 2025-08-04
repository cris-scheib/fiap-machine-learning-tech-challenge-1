from pydantic import BaseModel, Field

class BookSchema(BaseModel):
    id: int = Field(..., description="Unique book identifier")
    title: str = Field(..., description="Book title")
    price: float = Field(..., description="Book price")
    availability: str = Field(..., description="Book availability status")
    rating: str = Field(..., description="Book rating")
    category: str = Field(..., description="Book category")
    image_url: str = Field(..., description="Book image url")

    class Config:
        from_attributes = True