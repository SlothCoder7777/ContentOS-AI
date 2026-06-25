API_DESCRIPTION = """
ContentOS AI Backend is the production backend foundation for an AI-powered
content creation platform.

Current backend features include:

- JWT authentication
- User management foundation
- Brand memory foundation
- Neon PostgreSQL integration
- Alembic migrations
- Health checks
- System information endpoint
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
        "name": "Health",
        "description": "Application and database health check endpoints.",
    },
    {
        "name": "System",
        "description": "System metadata and backend information endpoints.",
    },
]
