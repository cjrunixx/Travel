export type City = {
  id: number;
  name: string;
  country: string;
  latitude?: number;
  longitude?: number;
};


const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export async function searchCities(search: string): Promise<City[]> {
  const query = new URLSearchParams({ search }).toString();
  const response = await fetch(`${API_BASE}/cities?${query}`);

  if (!response.ok) {
    throw new Error(`City search failed with status ${response.status}`);
  }

  return (await response.json()) as City[];
}
