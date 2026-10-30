# @title Cheese Catalog

pd.set_option("display.width", 140)
catalog = pd.DataFrame(load_json("catalog.json"))
catalog["price_per_100g"] = catalog["cents_per_100g"].map(lambda c: f"${c / 100:.2f}")
catalog["allergens"] = catalog["allergens"].str.join(", ")
catalog[["product_id", "name", "country", "style", "funk", "raw_milk", "price_per_100g", "stock_g", "allergens"]]
