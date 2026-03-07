import { useEffect, useRef, useState } from "react";
import type { City } from "../../api/cityApi";
import { searchCities } from "../../api/cityApi";

type Props = {
  id?: string;
  label: string;
  value: number;
  onChange: (cityId: number) => void;
};

export function CitySearchInput({ id, label, value, onChange }: Props) {
  const [query, setQuery] = useState("");
  const [selectedName, setSelectedName] = useState("");
  const [cities, setCities] = useState<City[]>([]);
  const [open, setOpen] = useState(false);
  const wrapRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (query.length < 2) { setCities([]); return; }
    const timer = setTimeout(() => {
      searchCities(query).then(setCities).catch(() => setCities([]));
    }, 300);
    return () => clearTimeout(timer);
  }, [query]);

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (wrapRef.current && !wrapRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  return (
    <div className="field" ref={wrapRef}>
      <label className="field-label" htmlFor={id}>{label}</label>
      <div className="city-search-wrap">
        <input
          id={id}
          type="text"
          value={query}
          placeholder={selectedName || "Type a city name…"}
          onChange={(e) => { setQuery(e.target.value); setOpen(true); }}
          onFocus={() => setOpen(true)}
          autoComplete="off"
        />
        {open && cities.length > 0 && (
          <ul className="city-dropdown" role="listbox">
            {cities.map((c) => (
              <li
                key={c.id}
                role="option"
                aria-selected={value === c.id}
                onClick={() => {
                  onChange(c.id);
                  setSelectedName(`${c.name}, ${c.country}`);
                  setQuery("");
                  setOpen(false);
                }}
              >
                <span>📍</span>
                {c.name}, <span style={{ color: "var(--text-3)", fontSize: 12 }}>{c.country}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
      {selectedName && (
        <span className="city-selected-tag">✓ {selectedName}</span>
      )}
    </div>
  );
}
