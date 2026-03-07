# System Design Notes

## Core Flow

1. User enters source, destination, dates, and budget.
2. Frontend calls `POST /api/v1/trips/plan`.
3. Planner service orchestrates transport, hotel, and attraction queries.
4. Planner ranks and returns aggregated recommendations.
5. User can save trip and manage selected attractions.

## Caching Targets

- City lookups
- Transport route searches
- Hotel search results

## Deferred Features

- Advisories with weather and disruption alerts
- Admin data management APIs
- AI recommendations (scikit-learn / PyTorch)
