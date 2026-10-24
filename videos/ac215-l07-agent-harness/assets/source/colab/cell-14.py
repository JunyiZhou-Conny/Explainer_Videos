# @title Store Policies
policy = load_json("policies.json")
rules = {
    "Cheeses per tasting":            f'{policy["min_products"]}–{policy["max_products"]} distinct',
    "Grams per guest":                f'{policy["min_grams_per_guest"]}–{policy["max_grams_per_guest"]} g',
    "Minimum per cheese":             f'{policy["min_product_grams"]} g, in {policy["quantity_increment_g"]} g steps',
    "Manager approval above":         f'${policy["manager_threshold_cents"] / 100:.0f} cheese subtotal',
    "Raw-milk shipping blocked to":   ", ".join(policy["raw_milk_blocked_states"]),
    "Revisions allowed":              policy["max_revisions"],
    "Approved vendor recipients":     ", ".join(policy["allowed_vendor_recipients"]),
}
pd.Series(rules, name="value").to_frame()
