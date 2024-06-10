from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import NullPool

from config import Settings


async_engine = create_async_engine(url=Settings.async_db_url(), echo=True, poolclass=NullPool)
async_session_maker = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session():
    async with async_session_maker() as session:
        yield session


class BaseModel(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow
    )
