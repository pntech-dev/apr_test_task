from elasticsearch import AsyncElasticsearch

INDEX_NAME = "documents"

INDEX_SETTINGS = {
    "settings": {
        "analysis": {
            "analyzer": {
                "russian_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "russian_stemmer"],
                }
            },
            "filter": {
                "russian_stemmer": {
                    "type": "stemmer",
                    "language": "russian",
                }
            },
        }
    },
    "mappings": {
        "properties": {
            "id": {"type": "integer"},
            "text": {"type": "text", "analyzer": "russian_analyzer"},
        }
    },
}


async def create_index(es: AsyncElasticsearch) -> None:
    if not await es.indices.exists(index=INDEX_NAME):
        await es.indices.create(index=INDEX_NAME, body=INDEX_SETTINGS)


async def search_documents(es: AsyncElasticsearch, query: str, size: int = 20) -> list[int]:
    resp = await es.search(
        index=INDEX_NAME,
        body={
            "query": {"match": {"text": query}},
            "size": size,
            "_source": False,
            "fields": ["id"],
        },
    )
    return [int(hit["fields"]["id"][0]) for hit in resp["hits"]["hits"]]
