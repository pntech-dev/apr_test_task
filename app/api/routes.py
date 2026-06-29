from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.db.elasticsearch import get_es_client
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.services.search import search_documents

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/search", response_model=list[DocumentResponse])
async def search(
    query: str = Query(..., description="Text search query"),
    session: AsyncSession = Depends(get_session),
    es=Depends(get_es_client),
):
    doc_ids = await search_documents(es, query, size=20)
    if not doc_ids:
        return []

    result = await session.execute(
        select(Document)
        .where(Document.id.in_(doc_ids))
        .order_by(Document.created_date)
    )
    return result.scalars().all()
