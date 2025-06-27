from fastapi import APIRouter
from app.controllers import health_controller, user_controller

router = APIRouter()
router.include_router(user_controller.router, prefix="/users", tags=["Users"])
router.include_router(health_controller.router, tags=["Health"])  
