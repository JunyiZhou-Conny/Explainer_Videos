from formaggio.agents.context import load_scenario
from formaggio.shop.store import Store
from formaggio.shop.data_models import LineItem

store, request = Store(), load_scenario("manager-approval")
cart = [("halloumi", 2000), ("walnut_chevre", 900), ("gouda", 1800), ("bucheron", 100)]
report = store.validate(request, [LineItem(product=p, grams=g) for p, g in cart])
print(report.total_grams, "g", report.subtotal_cents, "cents", "ok:", report.ok,
      "manager:", report.needs_manager_approval, [v.rule for v in report.violations])
