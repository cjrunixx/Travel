import type { Hotel } from "../../api/tripApi";

type Props = { hotel: Hotel };

function StarRating({ rating }: { rating: number }) {
  return (
    <div className="hotel-stars">
      {[1, 2, 3, 4, 5].map((star) => (
        <span key={star} className={star <= Math.round(rating) ? "" : "empty"}>★</span>
      ))}
      <span style={{ fontSize: 12, color: "var(--text-3)", marginLeft: 4 }}>
        {rating.toFixed(1)}
      </span>
    </div>
  );
}

export function HotelCard({ hotel }: Props) {
  return (
    <div className="hotel-card">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <div className="hotel-name">🏨 {hotel.name}</div>
      </div>
      <StarRating rating={hotel.rating} />
      <div>
        <span className="hotel-price">
          ₹{hotel.price_per_night.toLocaleString()}
          <span className="hotel-price-sub">/night</span>
        </span>
      </div>
    </div>
  );
}
