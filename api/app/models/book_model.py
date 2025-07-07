from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    price = Column(Float)
    availability = Column(String)
    rating = Column(String)
    category = Column(String)
