import ast
import asyncio
import csv
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session, engine
from app.db.base import Base
from app.models.document import Document


async def load_csv(path: str = "data/posts.csv") -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    rows: list[Document] = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rubrics = ast.literal_eval(row["rubrics"])
            created_date = datetime.strptime(row["created_date"], "%Y-%m-%d %H:%M:%S")
            rows.append(Document(text=row["text"], rubrics=rubrics, created_date=created_date))

    async with async_session() as session:
        session: AsyncSession
        session.add_all(rows)
        await session.commit()

    print(f"Loaded {len(rows)} documents")


if __name__ == "__main__":
    asyncio.run(load_csv())
