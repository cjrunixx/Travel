import { useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import type { TripPlanResponse } from "../../api/tripApi";

type Props = {
    trip: TripPlanResponse;
};

const ACCESS_TOKEN = import.meta.env.VITE_MAPBOX_API_KEY;

export function MapView({ trip }: Props) {
    const mapContainer = useRef<HTMLDivElement>(null);
    const map = useRef<mapboxgl.Map | null>(null);

    useEffect(() => {
        if (!mapContainer.current) return;
        if (!ACCESS_TOKEN || ACCESS_TOKEN === "replace_with_key") {
            console.warn("Mapbox API key is missing. Map will not render.");
            return;
        }

        mapboxgl.accessToken = ACCESS_TOKEN;

        const { source_city, destination_city, suggested_hotels, top_attractions } = trip;

        // Default to a world view if no coordinates
        const center: [number, number] = [
            destination_city.longitude ?? source_city.longitude ?? 0,
            destination_city.latitude ?? source_city.latitude ?? 0
        ];

        map.current = new mapboxgl.Map({
            container: mapContainer.current,
            style: "mapbox://styles/mapbox/dark-v11",
            center: center,
            zoom: 11,
        });

        map.current.addControl(new mapboxgl.NavigationControl(), "top-right");

        // Add markers
        const bounds = new mapboxgl.LngLatBounds();

        // Source Marker (Blue)
        if (source_city.longitude && source_city.latitude) {
            new mapboxgl.Marker({ color: "#3b82f6" })
                .setLngLat([source_city.longitude, source_city.latitude])
                .setPopup(new mapboxgl.Popup({ offset: 25 }).setHTML(`<h3>Origin: ${source_city.name}</h3>`))
                .addTo(map.current);
            bounds.extend([source_city.longitude, source_city.latitude]);
        }

        // Destination Marker (Purple)
        if (destination_city.longitude && destination_city.latitude) {
            new mapboxgl.Marker({ color: "#8b5cf6" })
                .setLngLat([destination_city.longitude, destination_city.latitude])
                .setPopup(new mapboxgl.Popup({ offset: 25 }).setHTML(`<h3>Destination: ${destination_city.name}</h3>`))
                .addTo(map.current);
            bounds.extend([destination_city.longitude, destination_city.latitude]);
        }

        // Hotel Markers (Teal)
        suggested_hotels.forEach((hotel) => {
            if (hotel.longitude && hotel.latitude) {
                new mapboxgl.Marker({ color: "#14b8a6", scale: 0.8 })
                    .setLngLat([hotel.longitude, hotel.latitude])
                    .setPopup(new mapboxgl.Popup({ offset: 25 }).setHTML(`<h4>🏨 ${hotel.name}</h4><p>₹${hotel.price_per_night}/night</p>`))
                    .addTo(map.current!);
                bounds.extend([hotel.longitude, hotel.latitude]);
            }
        });

        // Attraction Markers (Amber)
        top_attractions.forEach((attraction) => {
            if (attraction.longitude && attraction.latitude) {
                new mapboxgl.Marker({ color: "#f59e0b", scale: 0.8 })
                    .setLngLat([attraction.longitude, attraction.latitude])
                    .setPopup(new mapboxgl.Popup({ offset: 25 }).setHTML(`<h4>🎡 ${attraction.name}</h4><p>${attraction.category}</p>`))
                    .addTo(map.current!);
                bounds.extend([attraction.longitude, attraction.latitude]);
            }
        });

        // Draw Route Line
        if (source_city.longitude && source_city.latitude && destination_city.longitude && destination_city.latitude) {
            map.current.on("load", () => {
                map.current?.addSource("route", {
                    type: "geojson",
                    data: {
                        type: "Feature",
                        properties: {},
                        geometry: {
                            type: "LineString",
                            coordinates: [
                                [source_city.longitude!, source_city.latitude!],
                                [destination_city.longitude!, destination_city.latitude!],
                            ],
                        },
                    },
                });

                map.current?.addLayer({
                    id: "route",
                    type: "line",
                    source: "route",
                    layout: { "line-join": "round", "line-cap": "round" },
                    paint: { "line-color": "#3b82f6", "line-width": 4, "line-dasharray": [2, 1] },
                });
            });
        }

        if (!bounds.isEmpty()) {
            map.current.fitBounds(bounds, { padding: 50, maxZoom: 15 });
        }

        return () => map.current?.remove();
    }, [trip]);

    if (!ACCESS_TOKEN || ACCESS_TOKEN === "replace_with_key") {
        return (
            <div className="card" style={{ height: 400, display: "flex", alignItems: "center", justifyContent: "center", textAlign: "center", color: "var(--text-3)" }}>
                <div>
                    <p style={{ fontSize: 24, marginBottom: 12 }}>🗺</p>
                    <p>Maps are currently disabled.</p>
                    <p style={{ fontSize: 12, marginTop: 4 }}>Please provide a Mapbox API Key in your .env to see the interactive route.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="card" style={{ padding: 0, overflow: "hidden", marginBottom: 28 }}>
            <div ref={mapContainer} style={{ height: 400, width: "100%" }} />
        </div>
    );
}
