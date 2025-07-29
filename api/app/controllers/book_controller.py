from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.book_schema import BookSchema
from app.services.books_service import get_all_books, get_books_by_title_and_category, get_book_by_id
from app.core.auth import get_current_user
import logging


logger = logging.getLogger(__name__)
router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get("/",
         response_model=List[BookSchema],
         summary="List all books",
         description="Returns a list with all books registered in the system",
         status_code=status.HTTP_200_OK,
         responses={
             200: {"description": "Book list returned successfully"},
             404: {"description": "No books found"},
             500: {"description": "Internal server error"}
         })
async def list_books(db: Session = Depends(get_db)) -> List[BookSchema]:
    logger.info("Endpoint /books/ accessed - Listing all books")
    return get_all_books(db)

@router.get("/search",
         response_model=List[BookSchema],
         summary="Search books by title and category",
         description="Returns a list of books filtered by title and/or category",
         status_code=status.HTTP_200_OK,
         responses={
             200: {"description": "Filtered book list returned successfully"},
             404: {"description": "No books found with the provided criteria"},
             500: {"description": "Internal server error"}
         })
async def list_books_by_title_and_category(
    title: Optional[str] = Query(None, description="Title or part of the book title", min_length=1),
    category: Optional[str] = Query(None, description="Book category (optional)"),
    db: Session = Depends(get_db)
) -> List[BookSchema]:
    logger.info(f"Endpoint /books/search accessed - Searching books by title: '{title}' and category: '{category}'")
    books = get_books_by_title_and_category(db, title, category)
    return books

@router.get("/{id}",
         response_model=BookSchema,
         summary="Search book by ID",
         description="Returns the details of a specific book by its ID",
         status_code=status.HTTP_200_OK,
         responses={
             200: {"description": "Book found successfully"},
             404: {"description": "Book not found"},
             500: {"description": "Internal server error"}
         })
async def get_book(
    id: int = Path(..., title="Book ID", description="ID of the book to be searched", gt=0),
    db: Session = Depends(get_db)
) -> BookSchema:
    logger.info(f"Endpoint /books/{id} accessed - Searching book by ID")
    return get_book_by_id(db, id)

