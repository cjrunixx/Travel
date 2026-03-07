import type { TransportRoute } from "../../api/tripApi";

type Props = { route: TransportRoute };

const modeConfig: Record<string, { icon: string; cls: string; label: string }> = {
  train: { icon: "🚆", cls: "train", label: "Train" },
  flight: { icon: "✈", cls: "flight", label: "Flight" },
  bus: { icon: "🚌", cls: "bus", label: "Bus" },
  car: { icon: "🚗", cls: "car", label: "Car" },
};

export function RouteCard({ route }: Props) {
  const hours = Math.floor(route.duration / 60);
  const mins = route.duration % 60;
  const cfg = modeConfig[route.mode.toLowerCase()] ?? { icon: "🚀", cls: "train", label: route.mode };

  return (
    <div className="route-card">
      <div className={`route-icon ${cfg.cls}`}>{cfg.icon}</div>
      <div className="route-info">
        <div className="route-mode">{cfg.label}</div>
        <div className="route-meta">
          <span className="pill accent">⏱ {hours}h {mins}m</span>
          <span className="pill teal">₹{route.cost.toLocaleString()}</span>
          <span className="pill amber">
            {route.stops === 0 ? "Direct" : `${route.stops} stop${route.stops > 1 ? "s" : ""}`}
          </span>
        </div>
      </div>
    </div>
  );
}
