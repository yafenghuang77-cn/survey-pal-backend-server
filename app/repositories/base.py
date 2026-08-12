from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import EntityBase

ModelT = TypeVar("ModelT", bound=EntityBase)


class BaseRepository(Generic[ModelT]):
    def __init__(self, session: AsyncSession, model: type[ModelT]) -> None:
        self.session = session
        self.model = model

    async def get(self, entity_id: int) -> ModelT | None:
        statement = select(self.model).where(
            self.model.id == entity_id,
            self.model.is_deleted.is_(False),
        )
        return await self.session.scalar(statement)

    def add(self, entity: ModelT) -> ModelT:
        self.session.add(entity)
        return entity
