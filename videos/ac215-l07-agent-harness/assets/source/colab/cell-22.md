**Agent + Harness Layers**

The harness runs the same agent definition with four named layers:

- **Trace:** show and record what happened.
- **Budget:** limit model calls, tool calls, and runtime.
- **Context:** choose the extra information supplied to the agent.
- **CartCheck:** independently check the final proposed cart.

`build_agent` contains the agent definition shown above, with hooks for these layers. Calling `.run(...)` starts a fresh run using the chosen scenario.

The cart check finds problems; it does not repair the cart or place an order.
