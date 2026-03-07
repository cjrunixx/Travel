"""Seed the database with initial data for development."""

from app.config.database import SessionLocal, Base, engine
from app.models import *  # noqa: F401,F403

from app.models.city import City, Attraction
from app.models.transport import TransportMode, TransportRoute
from app.models.hotel import Hotel
from app.models.advisory import Advisory


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Skip if already seeded
        if db.query(City).first():
            print("Database already seeded — skipping.")
            return

        # ── Cities ──────────────────────────────────────────────
        cities = [
            City(name="Vadodara", country="India", latitude=22.3072, longitude=73.1812, timezone="Asia/Kolkata"),
            City(name="Goa", country="India", latitude=15.2993, longitude=74.1240, timezone="Asia/Kolkata"),
            City(name="Mumbai", country="India", latitude=19.0760, longitude=72.8777, timezone="Asia/Kolkata"),
            City(name="Delhi", country="India", latitude=28.7041, longitude=77.1025, timezone="Asia/Kolkata"),
            City(name="Jaipur", country="India", latitude=26.9124, longitude=75.7873, timezone="Asia/Kolkata"),
            City(name="Bangalore", country="India", latitude=12.9716, longitude=77.5946, timezone="Asia/Kolkata"),
            City(name="Kochi", country="India", latitude=9.9312, longitude=76.2673, timezone="Asia/Kolkata"),
            City(name="Udaipur", country="India", latitude=24.5854, longitude=73.7125, timezone="Asia/Kolkata"),
        ]
        db.add_all(cities)
        db.flush()

        # ── Transport Modes ─────────────────────────────────────
        modes = [
            TransportMode(name="flight"),
            TransportMode(name="train"),
            TransportMode(name="bus"),
            TransportMode(name="car"),
        ]
        db.add_all(modes)
        db.flush()

        mode_map = {m.name: m.id for m in modes}
        city_map = {c.name: c.id for c in cities}

        # ── Transport Routes ────────────────────────────────────
        routes = [
            # Vadodara → Goa
            TransportRoute(source_city_id=city_map["Vadodara"], destination_city_id=city_map["Goa"],
                           transport_mode_id=mode_map["train"], duration_minutes=540, distance_km=690, base_cost=1200, stops=0),
            TransportRoute(source_city_id=city_map["Vadodara"], destination_city_id=city_map["Goa"],
                           transport_mode_id=mode_map["bus"], duration_minutes=720, distance_km=690, base_cost=900, stops=2),
            TransportRoute(source_city_id=city_map["Vadodara"], destination_city_id=city_map["Goa"],
                           transport_mode_id=mode_map["flight"], duration_minutes=120, distance_km=690, base_cost=3500, stops=0),
            # Mumbai → Goa
            TransportRoute(source_city_id=city_map["Mumbai"], destination_city_id=city_map["Goa"],
                           transport_mode_id=mode_map["train"], duration_minutes=480, distance_km=580, base_cost=800, stops=1),
            TransportRoute(source_city_id=city_map["Mumbai"], destination_city_id=city_map["Goa"],
                           transport_mode_id=mode_map["flight"], duration_minutes=75, distance_km=580, base_cost=2500, stops=0),
            # Delhi → Jaipur
            TransportRoute(source_city_id=city_map["Delhi"], destination_city_id=city_map["Jaipur"],
                           transport_mode_id=mode_map["train"], duration_minutes=270, distance_km=280, base_cost=600, stops=0),
            TransportRoute(source_city_id=city_map["Delhi"], destination_city_id=city_map["Jaipur"],
                           transport_mode_id=mode_map["bus"], duration_minutes=330, distance_km=280, base_cost=450, stops=1),
            # Bangalore → Kochi
            TransportRoute(source_city_id=city_map["Bangalore"], destination_city_id=city_map["Kochi"],
                           transport_mode_id=mode_map["train"], duration_minutes=660, distance_km=560, base_cost=700, stops=2),
            TransportRoute(source_city_id=city_map["Bangalore"], destination_city_id=city_map["Kochi"],
                           transport_mode_id=mode_map["flight"], duration_minutes=65, distance_km=560, base_cost=2200, stops=0),
            # Delhi → Udaipur
            TransportRoute(source_city_id=city_map["Delhi"], destination_city_id=city_map["Udaipur"],
                           transport_mode_id=mode_map["flight"], duration_minutes=90, distance_km=660, base_cost=3000, stops=0),
            TransportRoute(source_city_id=city_map["Delhi"], destination_city_id=city_map["Udaipur"],
                           transport_mode_id=mode_map["train"], duration_minutes=720, distance_km=660, base_cost=900, stops=2),
        ]
        db.add_all(routes)
        db.flush()

        # ── Hotels ──────────────────────────────────────────────
        hotels = [
            # Goa
            Hotel(city_id=city_map["Goa"], name="Coastal Stay", price_per_night=2500, rating=4.3,
                  latitude=15.50, longitude=73.83, amenities="wifi,pool,breakfast", total_rooms=40),
            Hotel(city_id=city_map["Goa"], name="Budget Inn", price_per_night=1800, rating=4.0,
                  latitude=15.49, longitude=73.82, amenities="wifi,parking", total_rooms=25),
            Hotel(city_id=city_map["Goa"], name="Paradise Resort", price_per_night=5000, rating=4.7,
                  latitude=15.51, longitude=73.84, amenities="wifi,pool,breakfast,spa", total_rooms=60),
            # Jaipur
            Hotel(city_id=city_map["Jaipur"], name="Heritage Haveli", price_per_night=3000, rating=4.5,
                  latitude=26.92, longitude=75.78, amenities="wifi,breakfast,parking", total_rooms=30),
            Hotel(city_id=city_map["Jaipur"], name="Pink City Lodge", price_per_night=1500, rating=3.8,
                  latitude=26.91, longitude=75.79, amenities="wifi", total_rooms=20),
            # Kochi
            Hotel(city_id=city_map["Kochi"], name="Backwater Retreat", price_per_night=3500, rating=4.6,
                  latitude=9.94, longitude=76.26, amenities="wifi,pool,breakfast", total_rooms=35),
            Hotel(city_id=city_map["Kochi"], name="Fort House", price_per_night=2000, rating=4.2,
                  latitude=9.93, longitude=76.24, amenities="wifi,breakfast", total_rooms=18),
            # Udaipur
            Hotel(city_id=city_map["Udaipur"], name="Lake Palace Inn", price_per_night=4000, rating=4.8,
                  latitude=24.58, longitude=73.68, amenities="wifi,pool,breakfast,spa", total_rooms=50),
            Hotel(city_id=city_map["Udaipur"], name="Mewar Guest House", price_per_night=1200, rating=3.9,
                  latitude=24.57, longitude=73.69, amenities="wifi,parking", total_rooms=15),
            # Mumbai
            Hotel(city_id=city_map["Mumbai"], name="Sea View Hotel", price_per_night=4500, rating=4.4,
                  latitude=19.08, longitude=72.88, amenities="wifi,pool,breakfast", total_rooms=45),
        ]
        db.add_all(hotels)
        db.flush()

        # ── Attractions ─────────────────────────────────────────
        attractions = [
            # Goa
            Attraction(city_id=city_map["Goa"], name="Fort Aguada", category="historical",
                       description="17th-century Portuguese fort", rating=4.6, average_visit_time=90,
                       latitude=15.49, longitude=73.77),
            Attraction(city_id=city_map["Goa"], name="Baga Beach", category="nature",
                       description="Popular beach with water sports", rating=4.7, average_visit_time=180,
                       latitude=15.55, longitude=73.75),
            Attraction(city_id=city_map["Goa"], name="Basilica of Bom Jesus", category="cultural",
                       description="UNESCO World Heritage church", rating=4.5, average_visit_time=60,
                       latitude=15.50, longitude=73.91),
            Attraction(city_id=city_map["Goa"], name="Dudhsagar Falls", category="nature",
                       description="Four-tiered waterfall", rating=4.8, average_visit_time=240,
                       latitude=15.31, longitude=74.31),
            # Jaipur
            Attraction(city_id=city_map["Jaipur"], name="Hawa Mahal", category="historical",
                       description="Palace of Winds", rating=4.7, average_visit_time=60,
                       latitude=26.92, longitude=75.83),
            Attraction(city_id=city_map["Jaipur"], name="Amber Fort", category="historical",
                       description="Hilltop fort with stunning views", rating=4.8, average_visit_time=150,
                       latitude=26.98, longitude=75.85),
            Attraction(city_id=city_map["Jaipur"], name="City Palace", category="cultural",
                       description="Royal palace complex", rating=4.6, average_visit_time=120,
                       latitude=26.93, longitude=75.82),
            # Kochi
            Attraction(city_id=city_map["Kochi"], name="Chinese Fishing Nets", category="cultural",
                       description="Iconic shore-operated fishing nets", rating=4.3, average_visit_time=30,
                       latitude=9.97, longitude=76.24),
            Attraction(city_id=city_map["Kochi"], name="Fort Kochi Beach", category="nature",
                       description="Historic seaside promenade", rating=4.4, average_visit_time=90,
                       latitude=9.96, longitude=76.23),
            # Udaipur
            Attraction(city_id=city_map["Udaipur"], name="City Palace Udaipur", category="historical",
                       description="Palace complex on Lake Pichola", rating=4.9, average_visit_time=150,
                       latitude=24.58, longitude=73.68),
            Attraction(city_id=city_map["Udaipur"], name="Lake Pichola", category="nature",
                       description="Scenic lake with boat rides", rating=4.7, average_visit_time=120,
                       latitude=24.57, longitude=73.68),
            # Mumbai
            Attraction(city_id=city_map["Mumbai"], name="Gateway of India", category="historical",
                       description="Iconic arch monument", rating=4.5, average_visit_time=60,
                       latitude=18.92, longitude=72.83),
            Attraction(city_id=city_map["Mumbai"], name="Marine Drive", category="nature",
                       description="3.6-km promenade along the coast", rating=4.6, average_visit_time=90,
                       latitude=18.94, longitude=72.82),
        ]
        db.add_all(attractions)
        db.flush()

        # ── Advisories ──────────────────────────────────────────
        advisories = [
            Advisory(city_id=city_map["Goa"], category="weather", severity="moderate",
                     title="Heavy Rain Warning", description="Monsoon season expected mid-June to September",
                     source="IMD"),
            Advisory(city_id=city_map["Mumbai"], category="weather", severity="high",
                     title="Flood Risk Alert", description="Low-lying areas prone to waterlogging during monsoon",
                     source="IMD"),
            Advisory(city_id=city_map["Jaipur"], category="weather", severity="low",
                     title="Heat Wave Advisory", description="Temperatures may exceed 45°C in May-June",
                     source="IMD"),
        ]
        db.add_all(advisories)

        db.commit()
        print("Database seeded successfully.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
