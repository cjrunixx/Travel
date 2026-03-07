import type { TripPlanResponse } from "../../api/tripApi";
import { HotelCard } from "../../components/HotelCard";
import { RouteCard } from "../../components/RouteCard";
import { MapView } from "../../components/MapView";

const categoryIcon: Record<string, string> = {

  museum: "🏛",
  park: "🌿",
  beach: "🏖",
  restaurant: "🍽",
  temple: "⛩",
  monument: "🗽",
  nature: "🌄",
  entertainment: "🎢",
  shopping: "🛍",
  historical: "🏰",
};

function getAttractionIcon(category: string): string {
  const key = category.toLowerCase();
  for (const k of Object.keys(categoryIcon)) {
    if (key.includes(k)) return categoryIcon[k];
  }
  return "📍";
}

type Props = { result: TripPlanResponse };

export function TripResultsPage({ result }: Props) {
  return (
    <section className="card animate-in">
      <div className="results-header">
        <h2>Your Trip Plan</h2>
        <span className="trip-badge">#{result.trip_id}</span>
      </div>

      <MapView trip={result} />

      <div className="results-sections">

        {/* Transport */}
        <div>
          <p className="results-section-title">🚆 Recommended Transport</p>
          <RouteCard route={result.recommended_transport} />
        </div>

        <div className="divider" style={{ margin: "4px 0" }} />

        {/* Hotels */}
        <div>
          <p className="results-section-title">🏨 Suggested Hotels</p>
          {result.suggested_hotels.length === 0 ? (
            <div className="error-box">
              <span>💡</span> No hotels found within your budget. Try increasing it!
            </div>
          ) : (
            <div className="hotels-grid">
              {result.suggested_hotels.map((hotel) => (
                <HotelCard key={hotel.id} hotel={hotel} />
              ))}
            </div>
          )}
        </div>

        <div className="divider" style={{ margin: "4px 0" }} />

        {/* Attractions */}
        <div>
          <p className="results-section-title">🎡 Top Attractions</p>
          {result.top_attractions.length === 0 ? (
            <p style={{ color: "var(--text-3)", fontSize: 14 }}>No attractions found for this destination yet.</p>
          ) : (
            <ul className="attraction-list">
              {result.top_attractions.map((a) => (
                <li key={a.id} className="attraction-item">
                  <div className="attraction-icon">{getAttractionIcon(a.category)}</div>
                  <div className="attraction-info">
                    <div className="attraction-name">{a.name}</div>
                    <div className="attraction-meta">{a.category}</div>
                  </div>
                  <div className="attraction-rating">
                    ★ {a.rating.toFixed(1)}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </section>
  );
}
