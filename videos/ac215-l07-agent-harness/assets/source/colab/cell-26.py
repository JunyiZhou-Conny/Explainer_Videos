# Enriched Context

context_preview = preview_context(CONTEXT_SCENARIO)

print("📚 What changes before the first model call?")
print("Basic: the same shop rules, customer request, and tools; no extra context sources.")
for item in context_preview["enriched"]["sources"]:
    print(f"Enriched adds {item['source']}: {item['reason']}")

print("\nSaved preferences:", context_preview["enriched"]["sources"][-1]["content"].get("preferences", []))

print("\n🔎 Excluded from the enriched starting list:")
reason_labels = {
    "fictional_shipping_policy": "raw milk: blocked by the fictional destination policy",
    "allergen_conflict": "conflicts with the confirmed allergies",
    "insufficient_stock_for_minimum": "not enough stock for the minimum serving",
}
for product in context_preview["enriched"]["excluded_products"]:
    reasons = "; ".join(reason_labels.get(reason, reason) for reason in product["reasons"])
    print(f"- {product['product_id']}: {reasons}")
