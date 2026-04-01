from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.legacy import router as legacy_router


router = APIRouter()
router.include_router(health_router)
router.include_router(legacy_router)
