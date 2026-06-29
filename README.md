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
- Content project CRUD foundation
- Local AI content generation foundation
- Brand-aware content generation
- Content presets API
- WhatsApp campaign generator
- Trend detection foundation
- AI influencer generator
- Unified campaign generator
- Week 2 smoke tests

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
```
---

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
``
--- 


## Week 2 AI Foundation Features

Week 2 adds the first working AI-product foundation APIs.

### Content Projects

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/content-projects/presets` | Supported content types, platforms, and tones |
| POST | `/api/v1/content-projects` | Create a content project |
| GET | `/api/v1/content-projects` | List content projects |
| GET | `/api/v1/content-projects/{project_id}` | Get one content project |
| PATCH | `/api/v1/content-projects/{project_id}` | Update a content project |
| POST | `/api/v1/content-projects/{project_id}/generate` | Generate content for a project |
| DELETE | `/api/v1/content-projects/{project_id}` | Delete a content project |

### WhatsApp Campaigns

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/whatsapp-campaigns/generate` | Generate WhatsApp campaign message variations |

### Trends

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/trends/presets` | Supported trend detection presets |
| POST | `/api/v1/trends/detect` | Generate trend ideas for a niche/platform |

### AI Influencers

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/ai-influencers/presets` | Supported AI influencer presets |
| POST | `/api/v1/ai-influencers/generate` | Generate AI influencer persona and content direction |

### Unified Campaigns

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/campaigns/generate` | Generate campaign strategy, trend ideas, content variations, WhatsApp messages, and influencer direction |

## Week 3 Real AI Integration Features

Week 3 adds real AI integration foundations while keeping CI safe through mocked tests and safe fallback behavior.

### OpenAI / LLM

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/ai/status` | Safe AI provider configuration status |
| GET | `/api/v1/ai/health` | Safe AI provider health check |
| POST | `/api/v1/ai/generate` | Direct AI text generation using the LLM wrapper |

### LangGraph Agents

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/agents/content-workflow/run` | Run planner → writer → reviewer agent workflow |

### Week 3 Completed

- OpenAI GPT-5.5 environment configuration
- Secure API key handling through `.env`
- LLM service wrapper
- Mocked OpenAI tests
- Direct AI generation endpoint
- AI provider status endpoint
- AI provider health endpoint
- Prompt builder service
- AI generation mode for content projects
- Safe fallback when OpenAI is missing or fails
- LangGraph planner → writer → reviewer workflow
- AI-enhanced writer node with fallback
- Week 3 final smoke tests