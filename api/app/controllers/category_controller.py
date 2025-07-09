from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.category_service import get_all_categories
from app.schemas.category_schema import CategorySchema
from app.core.auth import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=List[CategorySchema])
def list_categories(db: Session = Depends(get_db)):
    return get_all_categories(db)