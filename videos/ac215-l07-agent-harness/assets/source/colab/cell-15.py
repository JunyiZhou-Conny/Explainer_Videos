# @title Pairings
pairings = pd.DataFrame(load_json("pairings.json"))
pairings["styles"] = pairings["styles"].str.join(", ")
pairings["allergens"] = pairings["allergens"].map(lambda a: ", ".join(a) or "—")
pairings[["name", "kind", "styles", "allergens"]]
