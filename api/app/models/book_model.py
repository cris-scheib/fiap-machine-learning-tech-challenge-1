from sqlalchemy import Column, Integer, String
from database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(String)
    availability = Column(String)
    rating = Column(String)
    category = Column(String)
