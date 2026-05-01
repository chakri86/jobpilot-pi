# AGENTS.md

Guidance for future Codex agents working on JobPilot Pi.

## Mission

Build and maintain a safe, local-first AI job assistant for Raspberry Pi. The product helps the user discover jobs, compare fit, draft materials, and manage application knowledge. It must not automate abusive or unauthorized activity on third-party job portals.

## Hard Rules

- Do not implement CAPTCHA bypass, stealth browsing, aggressive scraping, credential harvesting, or unauthorized auto-apply flows.
- Do not store LinkedIn, Indeed, or other job portal passwords.
- Do not expose OpenAI or provider API keys to the frontend.
- Do not commit `.env`, secrets, uploaded resumes, database files, or generated runtime logs.
- Keep application submission user-controlled.

## Architecture

- Backend: FastAPI, SQLAlchemy, Alembic, PostgreSQL.
- Frontend: React + Vite.
- Background jobs: APScheduler.
- AI: provider abstraction in `backend/app/ai`.
- Safe connectors: `backend/app/connectors`.
- Deployment: Docker Compose on Raspberry Pi OS.

## Development Standards

- Prefer small, descriptive commits.
- Add or update tests for changed backend behavior.
- Keep routers thin; place business logic in services.
- Use typed Python signatures.
- Keep frontend state simple and explicit.
- Validate external inputs and uploads.
- Keep documentation current with deployment changes.

## Branching

- `main`: production-ready.
- `dev`: active development.
- Feature branches should start from `dev`.

## Verification

Before handing off meaningful changes:

```bash
cd backend && pytest
cd frontend && npm run build
```

If dependencies are unavailable, document the exact command that could not be run.
