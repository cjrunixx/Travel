# System Architecture

## Style

- Monorepo
- Modular monolith backend (FastAPI)
- Local-first deployment in Docker Compose

## Layers

1. Presentation
   - React web app (`frontend`)
   - React Native placeholder (`mobile`)
2. API
   - FastAPI routers under `/api/v1`
3. Service
   - Planner, users/auth, transport, hotels, attractions
4. Data
   - PostgreSQL as system of record
   - Redis for read-heavy caching
5. Integration
   - Maps provider abstraction with free-tier provider configuration

## v1 Modules

- `auth`
- `users`
- `cities`
- `transport`
- `hotels`
- `attractions`
- `trips`

Deferred: advisories, admin, recommendations.
