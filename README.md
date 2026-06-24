# ContentOS AI Backend

ContentOS AI is a production-style FastAPI backend for an AI-powered content creation platform.

## Tech Stack

- Windows 11
- Python 3.13+
- FastAPI
- SQLAlchemy 2.x
- Alembic
- Pydantic v2
- JWT Authentication
- Neon PostgreSQL
- GitHub Actions

## Features Completed in Week 1

- Enterprise folder structure
- Environment configuration with Pydantic Settings v2
- Neon PostgreSQL connection
- SQLAlchemy database setup
- User model
- Brand model
- Alembic migrations
- Password hashing
- JWT access tokens
- Repository layer
- Service layer
- Protected routes
- Swagger API testing

## Project Structure

```text
contentos-ai/
├── app/
│   ├── api/
│   ├── core/
│   ├── dependencies/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
├── alembic/
├── tests/
├── requirements.txt
├── requirements-lock.txt
├── pyproject.toml
├── alembic.ini
├── .env.example
└── README.md