import type { Hotel } from "./tripApi";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export type HotelSearchParams = {
  city_id: number;
  min_price?: number;
  max_price?: number;
  rating?: number;
  sort?: string;
};

export async function searchHotels(params: HotelSearchParams): Promise<Hotel[]> {
  const query = new URLSearchParams();
  query.set("city_id", String(params.city_id));
  if (params.min_price !== undefined) query.set("min_price", String(params.min_price));
  if (params.max_price !== undefined) query.set("max_price", String(params.max_price));
  if (params.rating !== undefined) query.set("rating", String(params.rating));
  if (params.sort) query.set("sort", params.sort);

  const response = await fetch(`${API_BASE}/hotels?${query}`);
  if (!response.ok) throw new Error(`Hotel search failed (${response.status})`);
  return (await response.json()) as Hotel[];
}

export async function getHotel(hotelId: number): Promise<Hotel> {
  const response = await fetch(`${API_BASE}/hotels/${hotelId}`);
  if (!response.ok) throw new Error(`Hotel fetch failed (${response.status})`);
  return (await response.json()) as Hotel;
}
