from fastapi import APIRouter

from features.tasks.routes import router as tasks_router

router = APIRouter(prefix="/api/v1")

router.include_router(tasks_router, prefix="/tasks")


@router.get("/healthcheck")
def healthcheck():
    return {"status": "OK"}
