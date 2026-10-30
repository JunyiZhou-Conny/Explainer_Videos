# B13: is there a valid manager-approval cart under the $200 threshold? Store.validate, as every act uses it.
from formaggio.agents.context import load_scenario
from formaggio.shop.store import Store
from formaggio.shop.data_models import LineItem

store, request = Store(), load_scenario("manager-approval")
print("request:", request.party_size, "guests,", request.state, "budget", request.budget_cents, "allergies", request.allergies,
      "countries", request.required_countries, "min funk", request.required_min_funk)
print("policy: grams/guest", store.policy.min_grams_per_guest, "-", store.policy.max_grams_per_guest,
      "| cheeses", store.policy.min_products, "-", store.policy.max_products,
      "| step", store.policy.quantity_increment_g, "| min", store.policy.min_product_grams,
      "| approval above", store.policy.manager_threshold_cents)
for name, cart in {
    "fixture": [("comte", 1600), ("mimolette", 1600), ("taleggio", 1600)],
    "cheap": [("halloumi", 2000), ("walnut_chevre", 900), ("gouda", 1800), ("bucheron", 100)],
}.items():
    report = store.validate(request, [LineItem(product=p, grams=g) for p, g in cart])
    print(f"{name}: {report.total_grams} g, ${report.subtotal_cents / 100:.2f}, ok={report.ok}, "
          f"needs_manager_approval={report.needs_manager_approval}, violations={[v.rule for v in report.violations]}")
print("prices per 100 g:", {p: store.products[p].cents_per_100g for p in ("halloumi", "walnut_chevre", "gouda", "bucheron")},
      "| stock:", {p: store.inventory[p] for p in ("halloumi", "walnut_chevre", "gouda", "bucheron")})
