import type { City } from "./cityApi";

export type TripPlanRequest = {
  source_city_id: number;
  destination_city_id: number;
  start_date: string;
  end_date: string;
  budget: number;
};

export type TransportRoute = {
  route_id: number;
  mode: string;
  duration: number;
  cost: number;
  stops: number;
};

export type Hotel = {
  id: number;
  city_id: number;
  name: string;
  rating: number;
  price_per_night: number;
  latitude?: number;
  longitude?: number;
};

export type Attraction = {
  id: number;
  city_id: number;
  name: string;
  category: string;
  rating: number;
  latitude?: number;
  longitude?: number;
};

export type TripPlanResponse = {
  trip_id: number;
  source_city: City;
  destination_city: City;
  recommended_transport: TransportRoute;
  suggested_hotels: Hotel[];
  top_attractions: Attraction[];
};


const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export async function planTrip(payload: TripPlanRequest, token: string): Promise<TripPlanResponse> {
  const response = await fetch(`${API_BASE}/trips/plan`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? `Trip planning failed (${response.status})`);
  }

  return (await response.json()) as TripPlanResponse;
}
