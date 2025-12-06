## High-level checklist (prioritized)

1. Audit codebase and run tests/static analysis (in-progress)
Why: find quick wins and blockers before touching code.
Likely actions: run tests (pytest), run ruff/flake8/black, run mypy/pyright.
Files to inspect: main.py, config.py, services/*, utils/*.

2. Add type hints & data models
Use gradual typing, start with utils and services.
Prefer dataclasses or pydantic models for API responses/DTOs.

3. Refactor services into classes with small interfaces
Make each service a testable class (e.g., WeatherService, StocksService) implementing a small base interface.
Add dependency injection/factory used by main.py.

4. Centralize configuration & secrets
Move to pydantic.BaseSettings (settings.py) reading env vars and .env.
Add .env.example and document secret handling; don't commit secrets.

5. Improve HTTP usage & resiliency
Use httpx.AsyncClient (preferred) or requests.Session.
Add timeouts, retries/backoff (tenacity or httpx built-in), and graceful error handling.

6. Replace prints with structured logging
Configure logging from settings; consider JSON output for production.
Add log rotation.

7. Add formatting, linting, pre-commit hooks
Add ruff (or flake8), black, isort, pre-commit config in repo.

8. Add tests & CI
Add unit tests for utils and one service (mock external HTTP).
Add GitHub Actions workflow to run tests and linters.

9. Harden email sending
Use email.message.EmailMessage with text/HTML parts, inline images and attachments.
Add secure SMTP (starttls) and retries.

10. Add CLI entrypoint, packaging, Dockerfile, and docs
Small CLI (typer) to run reports manually; pyproject already exists—add console script.
Add Dockerfile and GitHub Action build if desired.
Improve README with setup, envs, and examples.

## Concrete, modern-python suggestions (code style & patterns)

- Use pathlib everywhere instead of os.path for file paths.
- Prefer dataclasses or pydantic for structured data (api responses, email payload).
- Add type hints to public functions and return types; use -> None or -> str as relevant.
- Use f-strings everywhere (if not already).
- Use context managers for files and network clients.
- Prefer httpx + async for IO-bound HTTP calls (gather multiple APIs concurrently).
- Centralize constants and magic strings (no inline API keys or endpoints).
- Use dependency injection for services to make them easily testable and swapable.
- Use exceptions with clear types and catch at boundaries (main CLI/runner).
- Validate external data and sanitize before building emails (avoid XSS in HTML parts).
- Add short docstrings for modules and public functions.

## Suggested minimal "contract" to keep in mind

- Inputs: environment variables (API keys, SMTP), optional CLI args (date range), external APIs (weather, headlines, stocks).
- Outputs: an email (text+HTML) sent via SMTP; logs and optionally a saved report file.
- Error modes: network errors (timeouts/retries), invalid API response, SMTP auth failures — these should fail gracefully and provide actionable logs.
- Success criteria: report produced and email sent; CI passes linting/tests; no secrets in repo.
