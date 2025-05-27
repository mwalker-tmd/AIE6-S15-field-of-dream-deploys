from fastapi import APIRouter
from backend.api.upload import router as upload_router
from backend.api.query import router as query_router

router = APIRouter()
router.include_router(upload_router)
router.include_router(query_router)
