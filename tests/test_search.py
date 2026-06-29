import pytest


@pytest.mark.anyio
async def test_search_returns_documents_ordered_by_date(client, mock_es, sample_docs):
    mock_es.search.return_value = {
        "hits": {"hits": [
            {"fields": {"id": [1]}},
            {"fields": {"id": [2]}},
        ]}
    }

    response = await client.get("/api/search", params={"query": "документ"})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == 2
    assert data[1]["id"] == 1
    assert data[0]["created_date"] < data[1]["created_date"]


@pytest.mark.anyio
async def test_search_empty_result(client, mock_es):
    mock_es.search.return_value = {"hits": {"hits": []}}

    response = await client.get("/api/search", params={"query": "несуществующий"})

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.anyio
async def test_search_requires_query_param(client):
    response = await client.get("/api/search")
    assert response.status_code == 422


@pytest.mark.anyio
async def test_search_response_has_all_fields(client, mock_es, sample_docs):
    mock_es.search.return_value = {
        "hits": {"hits": [{"fields": {"id": [1]}}]}
    }

    response = await client.get("/api/search", params={"query": "тест"})
    doc = response.json()[0]

    assert "id" in doc
    assert "text" in doc
    assert "rubrics" in doc
    assert "created_date" in doc
