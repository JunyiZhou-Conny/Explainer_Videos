# @title Catalog Data & Utils

#########################
# Data
#########################
CITIES = {
    "Seattle": {"airport": "SEA", "description": "Waterfront, markets, and museums."},
    "San Francisco": {"airport": "SFO", "description": "Bay views, parks, and neighborhoods."},
    "Los Angeles": {"airport": "LAX", "description": "Museums, beaches, and film attractions."},
}
HOTELS = {
    "SFO-BAY": ("San Francisco", "Bay Area Suite", 25000, True),
    "SFO-GATE": ("San Francisco", "Golden Gate Inn", 18000, False),
    "LAX-DOWNTOWN": ("Los Angeles", "LA Downtown Hotel", 22000, True),
    "LAX-HOLLYWOOD": ("Los Angeles", "Hollywood Stars Hotel", 17000, False),
    "SEA-HARBOR": ("Seattle", "Harbor Lodge", 20000, True),
    "SEA-CENTER": ("Seattle", "Seattle Downtown Hotel", 15000, False),
}
RESTAURANTS = [
    {"city": city, "name": f"{city} {cuisine} Kitchen", "cuisine": cuisine,
     "estimated_meal_usd": cost}
    for city in CITIES
    for cuisine, cost in [("Italian", 30), ("Mexican", 20), ("French", 45)]
]
ATTRACTIONS = {
    "SFO-BRIDGE": ("San Francisco", "Golden Gate Bridge", 0),
    "SFO-MUSEUM": ("San Francisco", "Bay Art Museum", 3000),
    "LAX-OBSERVATORY": ("Los Angeles", "Griffith Observatory grounds", 0),
    "LAX-MUSEUM": ("Los Angeles", "City Film Museum", 2500),
    "SEA-MARKET": ("Seattle", "Pike Place Market", 0),
    "SEA-MUSEUM": ("Seattle", "City Music Museum", 3000),
}

#########################
# Data Contracts
#########################
@dataclass
class TravelContext:
    # Agent's Travel context state
    checked_plan: dict | None = None
    budget_report: dict | None = None
    pending_proposal: dict | None = None
    approved_proposal: dict | None = None
    validated_this_turn: bool = False
    finalized_this_turn: bool = False

class PlannerReply(BaseModel):
    """The model must distinguish a final itinerary from a continuing turn."""
    kind: Literal["clarification", "options", "itinerary", "out_of_scope"]
    message: str

#########################
# Utils
#########################
OUTPUT_LOCK = threading.Lock()
MONEY_IN_PROSE = re.compile(r"\$\s*\d|\b\d+(?:\.\d+)?\s*(?:USD|dollars?)\b", re.IGNORECASE)

def canonical_city(value: str) -> str:
    for city in CITIES:
        if city.casefold() == value.strip().casefold():
            return city
    raise ValueError(f"Unsupported city {value!r}. Choose from {list(CITIES)}.")

def parse_date(value: str) -> date:
    return date.fromisoformat(value)

def flight_options(origin: str, destination: str, departure_date: str) -> list[dict]:
    origin, destination = canonical_city(origin), canonical_city(destination)
    if origin == destination:
        raise ValueError("Origin and destination must differ.")
    day = parse_date(departure_date)
    route = f"{CITIES[origin]['airport']}-{CITIES[destination]['airport']}"
    base = 15000 if {origin, destination} == {"San Francisco", "Los Angeles"} else 22000
    return [
        {"id": f"{route}-{day:%Y%m%d}-{i}", "origin": origin,
         "destination": destination, "date": day.isoformat(),
         "departure_local": hour, "airline": airline, "seats_available": 8,
         "price_basis": "per person, one way, economy, all-in mock fare",
         "price_cents": base + extra, "price_usd": (base + extra) / 100}
        for i, (hour, airline, extra) in enumerate([
            ("09:00", "Demo Air", 0), ("15:00", "Tutorial Airways", 5000)
        ], start=1)
    ]

def resolve_flight(flight_id: str) -> dict:
    parts = flight_id.split("-")
    if len(parts) != 4:
        raise ValueError("Use an exact flight ID returned by flight_search.")
    airports = {v["airport"]: k for k, v in CITIES.items()}
    origin, destination, raw_day, _ = parts
    if origin not in airports or destination not in airports:
        raise ValueError("Unknown airport in flight ID.")
    day = datetime.strptime(raw_day, "%Y%m%d").date().isoformat()
    for flight in flight_options(airports[origin], airports[destination], day):
        if flight["id"] == flight_id:
            return flight
    raise ValueError("Flight ID was not found in the mock catalog.")

def log_tool(name: str, details: str) -> None:
    with OUTPUT_LOCK:
        print(f"  [tool] {name}: {details}", flush=True)

def log_catalog(name: str, result: object) -> None:
    """Display canonical tool data instead of asking the model to repeat prices."""
    block = f"  [catalog] {name}:\n{json.dumps(result, indent=2)}"
    with OUTPUT_LOCK:
        print(block, flush=True)
