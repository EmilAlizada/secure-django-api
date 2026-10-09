# Secure Django API

[![CI / Security](https://github.com/EmilAlizada/secure-django-api/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/EmilAlizada/secure-django-api/actions/workflows/ci.yml)

A security-focused REST API built to demonstrate **authentication, authorization, secure configuration, data isolation, abuse resistance, testing, and security automation** in a compact Django codebase.

> Portfolio / learning project. The security decisions are intentionally documented so reviewers can inspect both the implementation and the reasoning.

## Security goals

This project is designed around a simple rule:

> Authentication proves who you are. Authorization decides what you are allowed to access.

The API therefore includes:

- JWT access and refresh tokens
- Django password validators and hashed password storage
- short-lived access tokens
- throttled authentication endpoints
- authenticated-by-default API policy
- owner-scoped querysets
- object-level authorization as a second boundary
- read-only ownership fields to prevent ownership spoofing
- debug mode disabled by default
- explicit allowed-host configuration
- secure cookie and browser-security settings
- non-root Docker runtime
- SAST, dependency auditing, linting, tests, and container scanning in CI

## API surface

| Method | Endpoint | Access | Purpose |
|---|---|---|---|
| GET | `/api/v1/health/` | Public | Service health |
| POST | `/api/v1/auth/register/` | Public / throttled | Create account |
| POST | `/api/v1/auth/token/` | Public / throttled | Obtain JWT pair |
| POST | `/api/v1/auth/token/refresh/` | Public / throttled | Refresh access token |
| GET | `/api/v1/me/` | Authenticated | Current user |
| GET/POST | `/api/v1/notes/` | Authenticated | List/create own notes |
| GET/PATCH/DELETE | `/api/v1/notes/{id}/` | Owner only | Manage own note |

## Authorization model

```text
Request
  |
  v
JWT authentication
  |
  v
Authenticated user
  |
  +--> Queryset filtered by owner
  |
  +--> Object-level IsOwner check
  |
  v
Allowed resource only
```

A user cannot retrieve another user's note by guessing its ID. The API intentionally returns `404` because unauthorized objects are excluded from the queryset before object access.

## Stack

| Area | Technology |
|---|---|
| Framework | Django 5.2 LTS |
| API | Django REST Framework |
| Authentication | Simple JWT |
| Database | PostgreSQL |
| Runtime | Gunicorn |
| Containers | Docker / Docker Compose |
| Tests | Pytest + pytest-django |
| Linting | Ruff |
| SAST | Bandit |
| Dependency audit | pip-audit |
| Container scan | Trivy |
| CI | GitHub Actions |

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

The API is available at:

```text
http://localhost:8000/api/v1/
```

### Register

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"emil","email":"emil@example.com","password":"StrongDemoPassword!42"}'
```

### Obtain a token

```bash
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"emil","password":"StrongDemoPassword!42"}'
```

Use the returned access token:

```bash
curl http://localhost:8000/api/v1/me/ \
  -H "Authorization: Bearer <access-token>"
```

See [docs/API.md](docs/API.md) for more examples.

## Project structure

```text
.
├── .github/
│   ├── dependabot.yml
│   └── workflows/ci.yml
├── api/
│   ├── migrations/
│   ├── auth_views.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── config/
├── docs/
│   ├── API.md
│   ├── ARCHITECTURE.md
│   └── THREAT_MODEL.md
├── Dockerfile
├── docker-compose.yml
├── SECURITY.md
└── requirements.txt
```

## Security testing

The test suite includes authorization tests that create data owned by two different users and verifies that one user:

- only sees their own records
- cannot retrieve another user's object
- cannot spoof the `owner` field during creation

Run locally:

```bash
pip install -r requirements-dev.txt
pytest -q
ruff check .
bandit -q -r api config -x api/tests.py
pip-audit -r requirements.txt
```

## CI security gates

Every push and pull request runs:

```text
Ruff
  -> Django system checks
  -> Pytest
  -> Bandit SAST
  -> pip-audit
  -> Docker build
  -> Trivy HIGH/CRITICAL image scan
```

## Documentation

- [API examples](docs/API.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Threat model](docs/THREAT_MODEL.md)
- [Security policy](SECURITY.md)

## Roadmap

- [ ] refresh-token revocation / blacklist support
- [ ] email verification flow
- [ ] structured security/audit events
- [ ] OpenAPI schema generation
- [ ] Redis-backed distributed throttling
- [ ] deployment behind a TLS-terminating reverse proxy

## Explore the portfolio

- [DevSecOps Pipeline](https://github.com/EmilAlizada/devsecops-pipeline)
- [Kubernetes Security Lab](https://github.com/EmilAlizada/kubernetes-security-lab)
- [Python Security Toolkit](https://github.com/EmilAlizada/python-security-toolkit)

[GitHub profile](https://github.com/EmilAlizada)

## Author

**Emil Alizada**  
Cybersecurity · DevOps · Secure Backend Engineering
