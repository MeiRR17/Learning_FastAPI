# Intermediate FastAPI Project

A FastAPI application with database integration and basic CRUD operations.

## Features

- **Database**: SQLAlchemy ORM with SQLite
- **CRUD Operations**: Create, Read, Update, Delete for items
- **Error Handling**: Basic HTTP exception handling
- **Auto-documentation**: Swagger UI and ReDoc automatically generated
- **Simple Structure**: Clean, easy-to-understand codebase

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn main:app --reload
```

The server will start on `http://localhost:8000`

## API Endpoints

### Items
- `GET /items/` - List all items, with optional `in_stock=true|false` filter and bounded pagination (`skip`, `limit`)
- `GET /items/{item_id}` - Get specific item
- `POST /items/` - Create new item
- `PUT /items/{item_id}` - Update item
- `DELETE /items/{item_id}` - Delete item

### System
- `GET /health` - Executes a real database query; returns HTTP 503 if SQLite is unavailable
- `GET /` - Welcome message

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: `http://localhost:8000/docs` - Interactive API testing
- **ReDoc**: `http://localhost:8000/redoc` - API documentation

## Database Model

### Item
- id (integer, primary key)
- name (string, indexed)
- description (string, optional)
- price (float)
- in_stock (boolean, default: True)
- created_at (datetime)

## Example Usage

1. Create an item:
```bash
curl -X POST "http://localhost:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Book", "description": "A good book", "price": 19.99}'
```

2. Get all items:
```bash
curl "http://localhost:8000/items/"
```

3. Update an item:
```bash
curl -X PUT "http://localhost:8000/items/1" \
  -H "Content-Type: application/json" \
  -d '{"price": 24.99}'
```

4. Delete an item:
```bash
curl -X DELETE "http://localhost:8000/items/1"
```

## Safer CRUD behavior (development branch)

The API accepts only nonblank item names of up to 120 characters, descriptions of up to 2,000 characters, and **non-negative finite prices**. New items may specify `in_stock` (default `true`). Partial `PUT /items/{item_id}` updates can omit fields; explicit JSON `null` is rejected for `name`, `price` and `in_stock`, rather than persisting values that break the response schema. An optional description can be cleared with `null`.

`GET /items/` lists **all** items by default, including out-of-stock items. Use `?in_stock=true` or `?in_stock=false` to filter. Pagination uses `skip=0` or greater and `limit=1..100`; it always orders by item ID so results are stable across requests. Invalid input produces the usual FastAPI/Pydantic 422 validation response.

```bash
curl "http://localhost:8000/items/?in_stock=false&skip=0&limit=25"
curl "http://localhost:8000/health"
```

The health endpoint now performs a real `SELECT 1` through SQLAlchemy and returns HTTP 503 when that query fails. This detects connectivity/query failures, not data consistency or general application readiness. The project is still an educational SQLite example, not a production-authenticated inventory service. This branch is awaiting owner-led testing and has not been merged.
