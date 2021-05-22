from fastapi import APIRouter
from api.controller import service

# Add routers
router = APIRouter()
router.include_router(service.router, tags=["service"])