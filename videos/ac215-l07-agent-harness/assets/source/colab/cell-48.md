## Act 6 — Agent Systems

**Question: Can the assistant use the governed ordering workflow, then turn its verified result into a complete tasting plan?**

The outer assistant calls the ordering workflow with `start_order`, then uses a skill to
explain the accepted menu. Check the authoritative order result and the tasting plan
separately. Cheeses, quantities and prices must agree with the receipt.

The manager scenario requires review only if the proposed subtotal exceeds $200.
A live model may choose a cheaper cart. Check that review actually happened before
claiming approval or refusal was tested. Each cell starts a fresh order.
