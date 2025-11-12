from fastapi import APIRouter

from app.api import nominees, nominations, results, votes


def get_api_router() -> APIRouter:
    """Этот роутер собирает все публичные маршруты API."""

    router = APIRouter(prefix="/api")
    router.include_router(nominations.router)
    router.include_router(nominees.router)
    router.include_router(votes.router)
    router.include_router(results.router)
    return router

