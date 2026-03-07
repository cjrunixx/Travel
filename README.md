# Travel Planner

Monorepo for a local-first, full-stack travel planning platform.

## Tech Stack

| Layer        | Technology                          |
|-------------|-------------------------------------|
| Frontend     | React 18 + TypeScript (Vite)        |
| Backend      | FastAPI (Python 3.12)               |
| Database     | PostgreSQL 16 (SQLAlchemy ORM)      |
| Cache        | Redis 7                             |
| Auth         | JWT (python-jose + bcrypt)          |
| Migrations   | Alembic                             |
| Maps         | Mapbox / Google Maps (configurable) |
| Mobile       | React Native (planned)              |
| DevOps       | Docker + Docker Compose             |

## Repository Layout

```
travel-planner/
├── backend/          FastAPI modular monolith
│   ├── app/
│   │   ├── config/       Settings, DB, Redis
│   │   ├── models/       SQLAlchemy ORM models
│   │   ├── schemas/      Pydantic request/response schemas
│   │   ├── repositories/ DB query layer
│   │   ├── services/     Business logic
│   │   ├── routers/      FastAPI endpoint handlers
│   │   └── utils/        JWT, password helpers
│   ├── alembic/          DB migration scripts
│   ├── seed.py           Development seed data
│   └── requirements.txt
├── frontend/         React + TypeScript (Vite)
│   └── src/
│       ├── api/           Fetch wrappers
│       ├── components/    Shared UI components
│       └── pages/         Route pages
├── mobile/           React Native (placeholder)
├── infrastructure/   Deployment configs and migrations
├── docs/             Architecture, schema, API spec
├── tests/            Cross-service tests
├── docker-compose.yml
└── .env.example
```

## API Domains (`/api/v1`)

| Domain           | Endpoints                                           |
|-----------------|-----------------------------------------------------|
| `/auth`          | POST /register, POST /login, GET /me               |
| `/users`         | GET /{id}, PUT /{id}/preferences                   |
| `/cities`        | GET ?search, GET /{id}                             |
| `/transport`     | GET /routes, GET /routes/{id}                      |
| `/hotels`        | GET ?city_id, GET /{id}                            |
| `/attractions`   | GET ?city_id, GET /{id}                            |
| `/trips`         | POST /plan, GET /{id}, POST /{id}/save             |
| `/advisories`    | GET ?city_id                                       |

Interactive docs: `http://localhost:8000/docs`

## Quick Start

1. Copy environment file:

```bash
cp .env.example .env
# Edit .env — set a strong JWT_SECRET_KEY and optionally map API keys
```

2. Start all services:

```bash
docker compose up --build
```

3. Seed the database with demo cities, hotels, routes and attractions:

```bash
docker compose --profile seed run --rm seed
```

4. Open:
   - Frontend: http://localhost:5173
   - API docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## Example User Flow

1. Register/Login → receive JWT token
2. Search cities by name using autocomplete
3. Submit trip plan (source city, destination, dates, budget)
4. Receive: recommended transport route, suggested hotels within budget, top-rated attractions
5. Save trip to your profile

## Current Scope (v1)

**Implemented:**
- Full authentication (register, login, JWT-protected endpoints)
- City search, transport routes, hotel search, attraction listing
- Planner service — aggregates transport + hotels + attractions into a trip plan
- Persistent storage in PostgreSQL (all data saved, not mocked)
- Advisory system (weather, disruption alerts per city)
- Redis cache infrastructure (client wired, ready for use)
- React frontend with city autocomplete and results display
- Full seed dataset: 8 cities, routes, hotels, attractions, advisories

**Deferred (later phases):**
- Admin CRUD APIs
- AI recommendations (scikit-learn / PyTorch)
- Map view (Mapbox / Google Maps integration)
- React Native mobile app
- Booking domain
- CI/CD pipeline

