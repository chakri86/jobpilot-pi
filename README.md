# JobPilot Pi

JobPilot Pi is a local-first AI job discovery and application assistant designed to run on a Raspberry Pi and stay accessible from your home network.

The MVP focuses on safe job discovery, matching, profile management, and assisted application drafting. It intentionally does not bypass CAPTCHA, evade portal protections, store job-board passwords, or auto-submit applications.

## Features

- Local authentication with a first-run bootstrap admin
- Profile management with resume upload validation
- URL-based job source management with configurable scan intervals
- Background job collection with safe mock connector support
- Deduplicated job storage in PostgreSQL
- AI-assisted job scoring, match explanations, missing skills, cover letters, resume suggestions, and answer drafts
- Q&A memory for reusable application answers
- React dashboard with jobs, filters, sources, profile, assistant, memory, and settings
- Docker Compose deployment for Raspberry Pi OS
- Alembic database migrations
- GitHub Actions for backend tests and frontend build checks

## Repository Layout

```text
backend/
  app/
    ai/
    connectors/
    models/
    routers/
    schemas/
    security/
    services/
    workers/
  alembic/
  tests/
frontend/
  src/
docs/
scripts/
.github/workflows/
```

## Quick Start

1. Copy the environment template:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set private values:

   ```env
   BOOTSTRAP_ADMIN_EMAIL=avkc@jobpilot.local
   BOOTSTRAP_ADMIN_PASSWORD=your-private-password
   SECRET_KEY=replace-with-a-long-random-secret
   ```

3. Start the app:

   ```bash
   docker compose up --build
   ```

4. Open:

   ```text
   http://192.168.0.249:5000
   ```

## Local Development

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

During local frontend development, Vite proxies `/api` calls to `http://localhost:5000`.

## Security Notes

- Never commit `.env` or real secrets.
- Bootstrap credentials are read from environment variables and stored only as password hashes.
- API keys stay server-side and are never returned to the browser.
- Resume uploads are validated by type and size.
- The app is intended for trusted local-network use and still requires login.
- Assisted Playwright workflows must stay user-controlled and must not auto-submit applications.

## Git Workflow

- `main` is production.
- `dev` is development.
- Feature branches should branch from `dev`.
- Pull requests should target `dev` first, then promote to `main` after validation.

## License

MIT. See [LICENSE](LICENSE).
