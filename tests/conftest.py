from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.base import Base
from app.db.elasticsearch import get_es_client
from app.db.session import get_session
from app.main import app
from app.models.document import Document

TEST_DB_URL = "postgresql+asyncpg://postgres:postgres%2Dpntech@localhost:5432/apr_test_task_test"


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def db_session():
    engine = create_async_engine(TEST_DB_URL, echo=False)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
def mock_es():
    return AsyncMock()


@pytest.fixture
async def client(db_session, mock_es):
    async def _override_session():
        yield db_session

    app.dependency_overrides[get_session] = _override_session
    app.dependency_overrides[get_es_client] = lambda: mock_es

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def sample_docs(db_session):
    docs = [
        Document(id=1, text="Первый тестовый документ", rubrics=["r1", "r2"], created_date=datetime(2024, 1, 10)),
        Document(id=2, text="Второй документ для поиска", rubrics=["r3"], created_date=datetime(2024, 1, 5)),
        Document(id=3, text="Третий документ удаление", rubrics=["r1"], created_date=datetime(2024, 1, 15)),
    ]
    db_session.add_all(docs)
    await db_session.commit()
    return docs
