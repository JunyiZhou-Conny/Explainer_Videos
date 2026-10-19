# @title Search Tools

#########################
# Tools
#########################
def city_search(city: str = "") -> dict:
    """List supported cities, or get information about one city; empty lists all."""
    log_tool("city_search", city or "all cities")
    if not city:
        result = {"cities": CITIES, "note": "Only these three cities are supported."}
    else:
        name = canonical_city(city)
        result = {"city": name, **CITIES[name]}
    log_catalog("city_search", result)
    return result

def flight_search(origin: str, destination: str, departure_date: str) -> list[dict]:
    """Search fictional one-way economy flights; date must be YYYY-MM-DD."""
    log_tool("flight_search", f"{origin} -> {destination}, {departure_date}")
    result = flight_options(origin, destination, departure_date)
    log_catalog("flight_search", result)
    return result

def hotel_search(city: str, check_in: str, check_out: str,
                 pet_friendly: bool = False) -> list[dict]:
    """Search one-room hotel stays, including exact cost for the requested nights."""
    name = canonical_city(city)
    nights = (parse_date(check_out) - parse_date(check_in)).days
    if nights <= 0:
        raise ValueError("Check-out must be after check-in.")
    log_tool("hotel_search", f"{name}, {nights} nights, pet-friendly={pet_friendly}")
    result = [{"id": key, "city": c, "name": title, "pet_friendly": pets,
               "nightly_usd": cents / 100, "nights": nights,
               "stay_total_usd": cents * nights / 100, "room_capacity": 2}
              for key, (c, title, cents, pets) in HOTELS.items()
              if c == name and (not pet_friendly or pets)]
    log_catalog("hotel_search", result)
    return result

def restaurant_search(city: str, cuisine: str = "") -> list[dict]:
    """Find fictional restaurants; optionally filter by Italian, Mexican, or French."""
    name = canonical_city(city)
    log_tool("restaurant_search", f"{name}, {cuisine or 'all cuisines'}")
    result = [r for r in RESTAURANTS if r["city"] == name
              and (not cuisine or r["cuisine"].casefold() == cuisine.strip().casefold())]
    log_catalog("restaurant_search", result)
    return result

def attraction_search(city: str) -> list[dict]:
    """List fictional attractions and admission prices per person per visit."""
    name = canonical_city(city)
    log_tool("attraction_search", name)
    result = [{"id": key, "name": title, "admission_usd": cents / 100}
              for key, (c, title, cents) in ATTRACTIONS.items() if c == name]
    log_catalog("attraction_search", result)
    return result
