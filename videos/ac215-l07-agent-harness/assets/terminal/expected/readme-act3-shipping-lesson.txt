# expected (README text, not program output): dlops-io/agent-harness, main @ e25dfe9615d78b78e0764a636cc2462f530a1402, README.md:369-402 (Live PA shipping lesson: what the before and after runs should show), unchanged.
### Live PA shipping lesson — Can the harness reject an invalid cart and help the model correct it?

Use **two live runs** with the same customer-submitted cart: Comté 350 g,
Bûcheron 350 g, and Époisses 300 g, destined for PA.

```bash
# Before: model records the customer's cart; the harness rejects it and stops.
python cli.py --act 3

# After: same input; the harness gives feedback and the live model revises it.
python cli.py --act 3 --scenario pa-shipping
```

The first command defaults to `pa-shipping-blocked`. It should show Comté marked
`RAW MILK`, a shipping violation, `WORKFLOW BLOCKED`, and no receipt.
The second should show the same initial violation, a second model call, `Removed:
Comté`, the model's replacement, and a validated order. If the model cannot produce
a valid revision, the harness stops without an order; no successful result is fabricated.

The starting cart is **customer input data**, in `data/shipping_customer_cart.json`.
It is not a prerecorded model response. The first model call records that cart
unchanged for downstream validation; an intake integrity check rejects a changed
cart rather than pretending the model followed the request. In the repair run,
subsequent model calls receive the normal policies, eligible catalog, previous cart,
and validation errors. Application code never selects the replacement.

Both runs enforce the same shipping policy. The before run stops at rejection; the
after run allows model revision. No policy is disabled to place an invalid order.
Orders are simulated and the PA rule is a fictional classroom policy.

For a normal live order without a submitted cart, use `--scenario standard`.
For the separate human-approval lesson, use `--scenario manager-approval` and respond
at the prompt. `--fixture` remains available for offline regression tests, but is
not needed for this live shipping demonstration.
