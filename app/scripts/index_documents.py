import asyncio

from sqlalchemy import select

from app.db.session import async_session
from app.db.elasticsearch import es_client
from app.models.document import Document
from app.services.search import INDEX_NAME, create_index


async def index_all() -> None:
    await create_index(es_client)

    async with async_session() as session:
        result = await session.execute(select(Document.id, Document.text))
        rows = result.all()

    actions = []
    for doc_id, text in rows:
        actions.append({"index": {"_index": INDEX_NAME, "_id": doc_id}})
        actions.append({"id": doc_id, "text": text})

    if actions:
        await es_client.bulk(body=actions, refresh=True)

    await es_client.close()
    print(f"Indexed {len(rows)} documents")


if __name__ == "__main__":
    asyncio.run(index_all())
