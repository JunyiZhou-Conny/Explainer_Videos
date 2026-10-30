# @title Data Constraints

# Apply the confirmed constraints to the shelf, one rule at a time.
raw = pd.DataFrame(load_json("catalog.json"))
blocked_states = policy["raw_milk_blocked_states"]

raw["raw-milk → PA"]   = raw["raw_milk"] & (request.state in blocked_states)
raw["nut allergen"]    = raw["allergens"].map(lambda a: "tree_nuts" in a or "peanut" in a)
raw["out of stock"]    = raw["stock_g"] < policy["min_product_grams"]
raw["eligible"]        = ~(raw["raw-milk → PA"] | raw["nut allergen"] | raw["out of stock"])
raw["French & funk≥4"] = raw["eligible"] & (raw["country"] == "France") & (raw["funk"] >= request.required_min_funk)

view = raw[["product_id", "country", "funk", "stock_g", "raw-milk → PA", "nut allergen", "out of stock", "eligible", "French & funk≥4"]]
flags = ["raw-milk → PA", "nut allergen", "out of stock"]
(view.style
     .map(lambda v: "background-color: #fde2e2" if v is True else "color: #bbb", subset=flags)
     .map(lambda v: "background-color: #dff5df" if v is True else "color: #bbb", subset=["eligible", "French & funk≥4"]))
