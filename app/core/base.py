"""Импорты класса Base и всех моделей для Alembic, чтобы не импортировать по отдельности."""

from app.core.database import Base  # noqa
from app.models.facebook_data import FacebookData, PixelToken  # noqa
