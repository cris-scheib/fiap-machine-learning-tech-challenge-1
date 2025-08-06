from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.category_service import get_all_categories
from app.core.auth import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/", response_model=List[str])
async def list_categories(db: Session = Depends(get_db)):
    categories = get_all_categories(db)
    return [category.category for category in categories]
