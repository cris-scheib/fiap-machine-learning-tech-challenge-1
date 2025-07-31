from sqlalchemy import Column, Integer, String
from app.core.database import Base
import logging

logger = logging.getLogger(__name__)

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    price = Column(String, nullable=False)
    availability = Column(String, nullable=False)
    rating = Column(String, nullable=True)
    category = Column(String, nullable=False, index=True)
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', category='{self.category}')>"
        
    def __str__(self):
        return f"Book: {self.title} (ID: {self.id})"
