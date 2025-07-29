from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.core.database import get_db
from app.core.auth import get_current_user
from app.services.stats_service import get_overview_stats, get_category_stats
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get("/overview",
            summary="Get general collection statistics",
            description="Returns general statistics such as total number of books, average price, and rating distribution.",
            status_code=status.HTTP_200_OK,
            responses={
                200: {"description": "Overview statistics returned successfully"},
                500: {"description": "Internal server error while generating overview"}
            })
async def stats_overview(db: Session = Depends(get_db)) -> Dict[str, Any]:
    logger.info("Endpoint /stats/overview accessed - Getting general book statistics")
    return get_overview_stats(db)

@router.get("/categories",
            summary="Get statistics by category",
            description="Returns statistics grouped by category, including number of books and average price per category.",
            status_code=status.HTTP_200_OK,
            responses={
                200: {"description": "Category statistics returned successfully"},
                500: {"description": "Internal server error while generating category stats"}
            })
async def stats_by_category(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    logger.info("Endpoint /stats/categories accessed - Getting statistics per book category")
    return get_category_stats(db)
