# **The Agent harness**

We now have a shop, its rules, and a customer with a request.

In this section we build the agent that serves that customer, and then wrap it in a harness
one layer at a time.

We keep the shopping request and constraints constant while changing how the system organizes reasoning, tools, and control.

Customer ask:

***Could you help me order cheese for a tasting for 12 guests in PA on a $150.00 budget? We need to avoid nuts. I'd like at least one cheese from France and at least one with a funk rating of 4 or higher. Could you suggest some pairings too?***

> As a rule of thumb: **the model proposes; the harness decides.**
Every time you see a result, ask which of the two produced it.
