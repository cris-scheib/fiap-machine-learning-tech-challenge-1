from fastapi import APIRouter
from app.controllers import health_controller, book_controller, user_controller, category_controller, stats_controller

router = APIRouter()
router.include_router(user_controller.router, prefix="/users", tags=["Users"])
router.include_router(book_controller.router, prefix="/api/v1/books", tags=["Books"])
router.include_router(category_controller.router, prefix="/api/v1/categories", tags=["Categories"])
router.include_router(stats_controller.router)
router.include_router(health_controller.router, tags=["Health"])
