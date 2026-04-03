# Docker Flask Postgres API

A production-ready REST API built with **Flask**, **PostgreSQL**, and **Docker Compose** — complete with migrations, a full test suite, and a GitHub Actions CI pipeline.

[![CI](https://github.com/donny-devops/docker-flask-postgres-api/actions/workflows/ci.yml/badge.svg)](https://github.com/donny-devops/docker-flask-postgres-api/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

---

## Architecture


---

## Quick Start

```bash
# 1. Clone and configure
git clone https://github.com/donny-devops/docker-flask-postgres-api.git
cd docker-flask-postgres-api
cp .env.example .env

# 2. Start all services
docker compose up -d

# 3. Run migrations
docker compose exec api flask db upgrade

# 4. Verify
curl http://localhost:5000/health
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/api/v1/items` | List all active items |
| `POST` | `/api/v1/items` | Create a new item |
| `GET` | `/api/v1/items/:id` | Get item by ID |
| `PUT` | `/api/v1/items/:id` | Update an item |
| `DELETE` | `/api/v1/items/:id` | Soft-delete an item |

### Request / Response Example

```bash
# Create an item
curl -X POST http://localhost:5000/api/v1/items \
  -H "Content-Type: application/json" \
  -d '{"name": "my-item", "description": "A sample item"}'

# Response
{
  "id": 1,
  "name": "my-item",
  "description": "A sample item",
  "is_active": true,
  "created_at": "2026-03-29T12:00:00+00:00",
  "updated_at": "2026-03-29T12:00:00+00:00"
}
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `production` | Flask environment mode |
| `SECRET_KEY` | *(required)* | Flask secret key |
| `DATABASE_URL` | `postgresql://...` | Full PostgreSQL connection string |
| `POSTGRES_USER` | `appuser` | PostgreSQL username |
| `POSTGRES_PASSWORD` | `apppassword` | PostgreSQL password |
| `POSTGRES_DB` | `appdb` | PostgreSQL database name |
| `PGADMIN_DEFAULT_EMAIL` | `admin@example.com` | pgAdmin login email |
| `PGADMIN_DEFAULT_PASSWORD` | `admin` | pgAdmin login password |

---

## Development

```bash
# Run tests locally
pip install -r requirements.txt
pytest --cov=app -v

# Lint
ruff check .
ruff format .

# Database migrations
flask db migrate -m "describe your change"
flask db upgrade
```

---

## Project Structure


---

## License

MIT — see [LICENSE](LICENSE).
