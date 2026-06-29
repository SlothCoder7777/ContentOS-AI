from app.core.constants import APP_NAME

API_DESCRIPTION = f"""
{APP_NAME} is the production backend foundation for an AI-powered
content creation platform.

Current backend features include:

- JWT authentication
- User management foundation
- Brand memory foundation
- Content project management
- OpenAI GPT-5.5 configuration
- LLM service wrapper
- Direct AI generation endpoint
- AI provider status and health endpoints
- Prompt builder service
- Local AI content generation foundation
- Brand-aware content generation
- AI generation mode with safe fallback
- WhatsApp campaign generation
- Trend detection foundation
- AI influencer generation
- Unified campaign generation
- LangGraph agent workflow foundation
- AI-enhanced agent workflow with fallback
- Neon PostgreSQL integration
- Alembic migrations
- Health checks
- System information endpoints
- CORS configuration
- Request logging
- Security headers
- Request ID tracing
- GitHub Actions CI
"""

OPENAPI_TAGS = [
    {
        "name": "Root",
        "description": "Base API overview endpoint.",
    },
    {
        "name": "Auth",
        "description": "Authentication endpoints for registration, login, and JWT access.",
    },
    {
        "name": "Users",
        "description": "User-related API operations.",
    },
    {
        "name": "Brands",
        "description": "Brand memory and brand profile API operations.",
    },
    {
        "name": "Content Projects",
        "description": "Create, manage, and generate content for content projects.",
    },
    {
        "name": "AI",
        "description": "Direct AI generation, AI health, and AI provider status endpoints.",
    },
    {
        "name": "Agents",
        "description": "LangGraph-powered AI agent workflow endpoints.",
    },
    {
        "name": "WhatsApp Campaigns",
        "description": "Generate WhatsApp campaign messages for offers and promotions.",
    },
    {
        "name": "Trends",
        "description": "Trend detection and content trend idea generation.",
    },
    {
        "name": "AI Influencers",
        "description": "Generate AI influencer personas and content directions.",
    },
    {
        "name": "Campaigns",
        "description": "Unified campaign generator combining trends, content, WhatsApp, and influencer direction.",
    },
    {
        "name": "Health",
        "description": "Application and database health check endpoints.",
    },
    {
        "name": "System",
        "description": "System metadata, route registry, and backend information endpoints.",
    },
]
