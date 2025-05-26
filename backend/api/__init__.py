from fastapi import APIRouter
from backend.api.upload import router as upload_router
from backend.api.query import router as query_router
from backend.api.agent import router as agent_router  # 👈 this line is often forgotten

router = APIRouter()
router.include_router(upload_router)
router.include_router(query_router)
router.include_router(agent_router)  # 👈 and this one
