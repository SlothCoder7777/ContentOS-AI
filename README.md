# ContentOS AI Backend

ContentOS AI is a FastAPI backend for an AI-powered content creation platform.

The backend currently includes authentication, user management foundation, brand memory foundation, PostgreSQL database integration, Alembic migrations, and GitHub Actions CI.

---

## Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic v2
- Neon PostgreSQL
- JWT Authentication
- Pytest
- GitHub Actions CI

---

## Project Status

Week 1 backend foundation is completed.

Completed setup:

- FastAPI backend
- Environment configuration
- Neon PostgreSQL connection
- SQLAlchemy setup
- User model
- Brand model
- JWT authentication
- Auth register/login flow
- FastAPI routers
- Alembic migrations
- Git repository setup
- GitHub Actions CI workflow

---

## Project Structure

```text
contentos-ai/
│
├── app/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   └── main.py
│
├── alembic/
│   └── versions/
│
├── tests/
│   └── test_app.py
│
├── .github/
│   └── workflows/
│       └── backend.yml
│
├── .env.example
├── .gitignore
├── alembic.ini
├── pytest.ini
├── requirements.txt
└── README.md

## Local Installation

Local Setup - Windows 11
1. Clone the repository
git clone YOUR_REPOSITORY_URL
cd contentos-ai
2. Create virtual environment
python -m venv .venv
3. Activate virtual environment
.venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Create .env

Copy .env.example and create a real .env file:

copy .env.example .env

Then update .env with your real Neon PostgreSQL URL and secret key.

Database Migration

Check current Alembic status:

alembic current

Apply migrations:

alembic upgrade head

Create a new migration after model changes:

alembic revision --autogenerate -m "describe migration"

Run Development Server
uvicorn app.main:app --reload

Open Swagger API docs:

http://127.0.0.1:8000/docs

Open ReDoc:

http://127.0.0.1:8000/redoc

Run Tests
pytest -q

## GitHub Actions CI

The backend CI workflow runs on:

Push to main or master
Pull requests to main or master
Manual workflow dispatch

The workflow checks:

Python 3.13 setup
Dependency installation
Required secrets
FastAPI import
Alembic migration state
Alembic upgrade
Python source compilation
Pytest test suite

Required GitHub repository secrets:

DATABASE_URL
SECRET_KEY

Add them in:

GitHub Repository → Settings → Secrets and variables → Actions
