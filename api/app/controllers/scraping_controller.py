from fastapi import APIRouter, BackgroundTasks, Depends, status, HTTPException
from app.core.auth import get_current_user
from app.services.scrapper.scrapper_service import run_scraping
import logging

logger = logging.getLogger(__name__)
router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.post(
    "/trigger",
    response_model=str,
    status_code=status.HTTP_202_ACCEPTED,
)
async def trigger_scraping(
    background_tasks: BackgroundTasks
):
    try:
        background_tasks.add_task(run_scraping)
        return {"message": "Scraping agendado com sucesso."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao agendar scraping: {e}"
        )