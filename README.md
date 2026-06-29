# Document Search API

REST API для хранения документов в PostgreSQL с полнотекстовым поиском через Elasticsearch.

**Стек:** FastAPI, PostgreSQL, Elasticsearch, Docker

## Быстрый старт (Docker)

```bash
git clone <repo-url>
cd apr_test_task
docker-compose up --build
```

API будет доступен по адресу `http://localhost:8000`.

После запуска контейнеров загрузите данные и создайте поисковый индекс:

```bash
docker-compose exec app python -m app.scripts.load_csv
docker-compose exec app python -m app.scripts.index_documents
```

## Локальная разработка

### Требования

- Python 3.10+
- PostgreSQL 16
- Elasticsearch 8.x

### Установка

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

pip install -r requirements.txt
```

Скопируйте `.env.example` в `.env` и укажите пароль от базы данных:

```bash
cp .env.example .env
```

Создайте базу данных:

```bash
psql -U postgres -c "CREATE DATABASE apr_test_task"
```

Загрузите данные и создайте индекс:

```bash
python -m app.scripts.load_csv
python -m app.scripts.index_documents
```

Запустите сервер:

```bash
uvicorn app.main:app --reload
```

## API эндпоинты

### Проверка состояния

```
GET /api/health
```

### Поиск документов

```
GET /api/search?query=<текст>
```

Возвращает до 20 документов, соответствующих запросу, отсортированных по дате создания. Каждый документ содержит поля `id`, `text`, `rubrics` и `created_date`.

### Удаление документа

```
DELETE /api/documents/{id}
```

Удаляет документ из PostgreSQL и из индекса Elasticsearch. Возвращает 404, если документ не найден.

## Тесты

```bash
pytest tests/ -v
```

Тесты используют отдельную базу `apr_test_task_test` и мокают Elasticsearch.

## Структура проекта

```
app/
  api/          - Роуты API
  core/         - Конфигурация
  db/           - Клиенты БД и Elasticsearch
  models/       - SQLAlchemy модели
  schemas/      - Pydantic схемы
  services/     - Бизнес-логика
  scripts/      - Скрипты загрузки данных
tests/          - Функциональные тесты
data/           - Исходные CSV данные
```
