# Database Schema Overview

## Core Entities (v1)

- `users`
- `user_preferences`
- `cities`
- `attractions`
- `transport_modes`
- `transport_routes`
- `hotels`
- `trips`
- `trip_transport`
- `trip_hotels`
- `trip_attractions`

## Indexing (v1)

- `cities(name)`
- `transport_routes(source_city_id, destination_city_id)`
- `hotels(city_id)`
- `attractions(city_id)`

## Notes

- Schema is normalized around `cities` to avoid duplicate city data.
- Advisory and booking tables are deferred from initial migration set.
