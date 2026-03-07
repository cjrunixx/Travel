import { FormEvent, useState } from "react";
import type { TripPlanRequest } from "../../api/tripApi";
import { CitySearchInput } from "../../components/CitySearchInput";

type Props = {
  onSubmit: (payload: TripPlanRequest) => Promise<void>;
  loading: boolean;
};

export function TripPlannerPage({ onSubmit, loading }: Props) {
  const [sourceCityId, setSourceCityId] = useState(0);
  const [destinationCityId, setDestinationCityId] = useState(0);
  const today = new Date().toISOString().split("T")[0];
  const threeDaysFromNow = new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString().split("T")[0];
  const [startDate, setStartDate] = useState(today);
  const [endDate, setEndDate] = useState(threeDaysFromNow);
  const [budget, setBudget] = useState(10000);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await onSubmit({
      source_city_id: sourceCityId,
      destination_city_id: destinationCityId,
      start_date: startDate,
      end_date: endDate,
      budget,
    });
  };

  const canSubmit = sourceCityId !== 0 && destinationCityId !== 0 && !loading;

  return (
    <section className="card animate-in">
      <h2 className="card-title">
        <span className="icon" style={{ background: "rgba(59,130,246,0.15)" }}>🗺</span>
        Plan Your Trip
      </h2>

      <form className="form-grid" onSubmit={handleSubmit}>
        <div className="form-row">
          <CitySearchInput
            id="source-city"
            label="🛫 Origin City"
            value={sourceCityId}
            onChange={setSourceCityId}
          />
          <CitySearchInput
            id="destination-city"
            label="🛬 Destination City"
            value={destinationCityId}
            onChange={setDestinationCityId}
          />
        </div>

        <div className="form-row">
          <div className="field">
            <label className="field-label" htmlFor="start-date">📅 Departure Date</label>
            <input
              id="start-date"
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              required
            />
          </div>
          <div className="field">
            <label className="field-label" htmlFor="end-date">📅 Return Date</label>
            <input
              id="end-date"
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              required
            />
          </div>
        </div>

        <div className="field">
          <label className="field-label" htmlFor="budget">💰 Budget (₹)</label>
          <input
            id="budget"
            type="number"
            value={budget}
            onChange={(e) => setBudget(Number(e.target.value))}
            min={0}
            required
            placeholder="10000"
          />
        </div>

        <button
          id="plan-trip-btn"
          type="submit"
          className="btn btn-primary btn-full"
          disabled={!canSubmit}
          style={{ marginTop: 8 }}
        >
          {loading ? (
            <><div className="spinner" /> Finding the best routes…</>
          ) : "✨ Plan My Trip"}
        </button>
      </form>
    </section>
  );
}
