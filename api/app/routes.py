from fastapi import APIRouter
from app.controllers import health_controller, book_controller, user_controller

router = APIRouter()
router.include_router(user_controller.router, prefix="/users", tags=["Users"])
router.include_router(book_controller.router, prefix="/api/v1", tags=["Books"])
router.include_router(health_controller.router, tags=["Health"])  