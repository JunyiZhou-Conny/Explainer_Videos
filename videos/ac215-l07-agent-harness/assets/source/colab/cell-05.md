# **Understanding Agent Harness**

**What Is an Agent Harness?**<br>
---
A model on its own is just a function from text to text. It can read a prompt and produce a completion — and that is all it can do. It cannot call an API, read a file, remember yesterday, or check whether its own answer was correct.

An **agent harness** is the software wrapped around the model that turns that function into something that can actually do work:

> *"The software scaffolding around a model: the loop, tools, context management, and guardrails that turn raw intelligence into a working agent."* — Anthropic

**What we'll build**

We start with the smallest thing that works — an agent with instructions, a few tools, and a customer who wants cheese — and keep that agent fixed.

Then we add each concern (tracing, budgets, context, validation, and later approvals and memory) as a layer around it, and watch what each one adds to the record of what actually happened. By the end, you'll be able to understand how agent harness works.
