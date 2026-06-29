import pytest
from sqlalchemy import select

from app.models.document import Document


@pytest.mark.anyio
async def test_delete_document(client, mock_es, sample_docs, db_session):
    response = await client.delete("/api/documents/1")

    assert response.status_code == 200
    assert response.json()["detail"] == "Document 1 deleted"

    result = await db_session.execute(select(Document).where(Document.id == 1))
    assert result.scalar_one_or_none() is None

    mock_es.delete.assert_called_once()


@pytest.mark.anyio
async def test_delete_nonexistent_document(client, mock_es):
    response = await client.delete("/api/documents/9999")

    assert response.status_code == 404
    mock_es.delete.assert_not_called()
