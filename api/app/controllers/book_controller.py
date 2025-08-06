from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.book_schema import BookSchema
from app.services.books_service import get_all_books, get_books_by_title_and_category, get_book_by_id, get_top_rated_books, get_books_by_price_range
from app.core.auth import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/",
            response_model=List[BookSchema],
            status_code=status.HTTP_200_OK,
            )
async def list_books(db: Session = Depends(get_db)) -> List[BookSchema]:
    logger.info("Endpoint /books/ accessed - Listing all books")
    return get_all_books(db)


@router.get("/search",
            response_model=List[BookSchema],
            status_code=status.HTTP_200_OK,
            )
async def list_books_by_title_and_category(
        title: Optional[str] = Query(None, description="Title or part of the book title"),
        category: Optional[str] = Query(None, description="Book category (optional)"),
        db: Session = Depends(get_db)
) -> List[BookSchema]:
    logger.info(f"Endpoint /books/search accessed - Searching books by title: '{title}' and category: '{category}'")
    books = get_books_by_title_and_category(db, title, category)
    return books


@router.get("/top-rated",
            response_model=List[BookSchema],
            status_code=status.HTTP_200_OK
            )
async def top_rated_books(
        limit: int = Query(10, description="Number of top books to return"),
        db: Session = Depends(get_db)
) -> List[BookSchema]:
    logger.info("Endpoint /books/top-rated accessed")
    return get_top_rated_books(db, limit)


@router.get("/price-range",
            response_model=List[BookSchema],
            status_code=status.HTTP_200_OK)
async def books_by_price_range(
        min: float = Query(..., description="Minimum price"),
        max: float = Query(..., description="Maximum price"),
        db: Session = Depends(get_db)
) -> List[BookSchema]:
    logger.info(f"Endpoint /books/price-range accessed with min={min}, max={max}")
    return get_books_by_price_range(db, min, max)


@router.get("/{id}",
            response_model=BookSchema,
            status_code=status.HTTP_200_OK,
            )
async def get_book(
        id: int = Path(..., title="Book ID", description="ID of the book to be searched", gt=0),
        db: Session = Depends(get_db)
) -> BookSchema:
    logger.info(f"Endpoint /books/{id} accessed - Searching book by ID")
    return get_book_by_id(db, id)
