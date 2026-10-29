# Q3 and B6: what the approval fingerprint covers (checkout.py:28-37), computed directly.
from formaggio.agents.context import load_scenario
from formaggio.shop.checkout import Checkout
from formaggio.shop.data_models import LineItem

checkout = Checkout()
request = load_scenario("manager-approval")
cart = [LineItem(product="comte", grams=1600), LineItem(product="mimolette", grams=1600),
        LineItem(product="taleggio", grams=1600)]


def fp(items=cart, req=request):
    return checkout.fingerprint(req, checkout.store.validate(req, items))[:16]

print("approved cart           ", fp())
checkout.store.inventory["mimolette"] = 1400
print("after stock 3000 -> 1400", fp(), "| still valid?", checkout.store.validate(request, cart).ok)
checkout.store.inventory["mimolette"] = 3000
reordered = [cart[2], cart[0], cart[1]]
print("same lines, other order ", fp(reordered))
print("taleggio 1600 -> 1650 g ", fp([*cart[:2], LineItem(product="taleggio", grams=1650)]))
print("one more guest (61)     ", fp(req=request.model_copy(update={"party_size": 61})))
checkout.store.products["mimolette"] = checkout.store.products["mimolette"].model_copy(update={"cents_per_100g": 501})
print("mimolette price +1 cent ", fp())
