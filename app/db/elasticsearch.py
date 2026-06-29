from elasticsearch import AsyncElasticsearch

from app.core.config import settings

es_client = AsyncElasticsearch(settings.elasticsearch_url)


async def get_es_client() -> AsyncElasticsearch:
    return es_client
