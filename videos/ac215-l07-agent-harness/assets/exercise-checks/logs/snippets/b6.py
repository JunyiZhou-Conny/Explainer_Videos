from formaggio.agents.context import load_scenario
from formaggio.shop.checkout import Checkout
from formaggio.shop.data_models import LineItem

checkout = Checkout()
request = load_scenario("manager-approval")
cart = [LineItem(product="comte", grams=1600), LineItem(product="mimolette", grams=1600),
        LineItem(product="taleggio", grams=1600)]


def fp(items=cart, req=request):
    return checkout.fingerprint(req, checkout.store.validate(req, items))[:16]

print("approved cart       ", fp())
checkout.store.inventory["mimolette"] = 1400
print("(a) stock 1,400 g   ", fp())
checkout.store.inventory["mimolette"] = 3000
print("(b) lines reordered ", fp([cart[2], cart[0], cart[1]]))
print("(c) taleggio 1650 g ", fp([cart[0], cart[1], LineItem(product="taleggio", grams=1650)]))
print("(d) 61 guests       ", fp(req=request.model_copy(update={"party_size": 61})))
checkout.store.products["mimolette"] = checkout.store.products["mimolette"].model_copy(update={"cents_per_100g": 501})
print("(e) price +1 cent   ", fp())
