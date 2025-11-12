import asyncio
import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.router import get_api_router
from app.core.config import settings
from app.telegram_bot.runner import start_polling

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Эта функция создаёт и настраивает экземпляр FastAPI."""

    app = FastAPI(title=settings.app_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(get_api_router())

    # Раздача медиафайлов (загруженные изображения)
    media_dir = Path(settings.media_folder)
    media_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/media", StaticFiles(directory=str(media_dir)), name="media")

    # Раздача статических файлов фронтенда
    static_dir = Path(__file__).resolve().parent / "static"
    if static_dir.exists():
        app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")
        
        @app.get("/{full_path:path}")
        async def serve_spa(request: Request, full_path: str):
            """Раздача SPA - все несуществующие роуты перенаправляем на index.html"""
            # Если это API запрос, пропускаем
            if full_path.startswith("api/") or full_path.startswith("media/"):
                return {"detail": "Not Found"}
            
            # Проверяем, существует ли файл
            file_path = static_dir / full_path
            if file_path.is_file():
                return FileResponse(file_path)
            
            # Для всех остальных путей возвращаем index.html (для SPA роутинга)
            return FileResponse(static_dir / "index.html")

    @app.on_event("startup")
    async def startup_event() -> None:
        """Эта функция запускает Telegram-бота при старте приложения."""

        if settings.telegram_bot_token:
            logger.info("Starting Telegram bot...")
            asyncio.create_task(start_polling())
        else:
            logger.warning("TELEGRAM_BOT_TOKEN not set, bot will not start")

    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        """Этот эндпоинт говорит, что сервис жив и готов работать."""

        return {"status": "ok"}

    return app


app = create_app()

