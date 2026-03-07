# API Specification (v1)

Base prefix: `/api/v1`

All protected endpoints require `Authorization: Bearer <token>` header.

## Health

- `GET /health` — Returns `{"status": "ok", "environment": "..."}` (public)

## Auth (public)

- `POST /auth/register` — `{ name, email, password }` → `{ access_token, user_id }`
- `POST /auth/login` — `{ email, password }` → `{ access_token, user_id }`
- `GET /auth/me` — 🔒 Returns current user profile

## Users 🔒

- `GET /users/{user_id}` — Get user profile
- `PUT /users/{user_id}/preferences` — `{ budget_preference, preferred_transport, travel_style?, alerts_enabled }`

## Cities (public)

- `GET /cities?search=<term>` — Search cities by name
- `GET /cities/{city_id}` — Get city by ID

## Transport (public)

- `GET /transport/routes?source_city_id=&destination_city_id=&transport_mode=` — Search routes
- `GET /transport/routes/{route_id}` — Get route details

## Hotels (public)

- `GET /hotels?city_id=&min_price=&max_price=&rating=&sort=price` — Search hotels
- `GET /hotels/{hotel_id}` — Get hotel details

## Attractions (public)

- `GET /attractions?city_id=` — Get attractions for a city
- `GET /attractions/{attraction_id}` — Get attraction details

## Trips 🔒

- `POST /trips/plan` — `{ source_city_id, destination_city_id, start_date, end_date, budget }` → trip plan
- `GET /trips/{trip_id}` — Get saved trip details
- `POST /trips/{trip_id}/save` — Confirm/save trip
- `POST /trips/{trip_id}/attractions?attraction_id=` — Add attraction to trip

## Advisories (public)

- `GET /advisories?city_id=` — Get travel advisories for a city

## Planned (Future)

- `GET /recommendations/routes` — AI-ranked route suggestions
- `GET /recommendations/hotels` — Personalized hotel recommendations
- `POST /admin/hotels` — Admin: add hotel
- `POST /admin/attractions` — Admin: add attraction

