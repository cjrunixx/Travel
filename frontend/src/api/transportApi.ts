import type { TransportRoute } from "./tripApi";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export type RouteSearchParams = {
  source_city_id: number;
  destination_city_id: number;
  transport_mode?: string;
};

export async function searchRoutes(params: RouteSearchParams): Promise<TransportRoute[]> {
  const query = new URLSearchParams({
    source_city_id: String(params.source_city_id),
    destination_city_id: String(params.destination_city_id),
  });
  if (params.transport_mode) query.set("transport_mode", params.transport_mode);

  const response = await fetch(`${API_BASE}/transport/routes?${query}`);
  if (!response.ok) throw new Error(`Route search failed (${response.status})`);
  return (await response.json()) as TransportRoute[];
}
