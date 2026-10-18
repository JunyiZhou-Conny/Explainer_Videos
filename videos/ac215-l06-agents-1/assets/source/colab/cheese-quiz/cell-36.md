We have already seen a basic prompt in the previous section, but here we deliberately build again from the basic prompt. This time, the goal is different: instead of comparing an LLM with an agent, we hold the model and question constant so we can isolate the effect of each additional piece of context. Starting from zero gives us a clean baseline, and then we add one layer at a time.

To understand how model context works let us use the same sample cheese question: **What's the best cheese for a grilled cheese sandwich?**

We will ask this same question to an LLM while incrementally adjusting the context, and compare the results from each step.

* Step 1: Basic prompt
* Step 2: Prompt Engineering
* Step 3: Retrieve Relevant Documents (e.g. RAG)
* Step 4: Adding Short-term Memory
* Step 5: Adding Long-term Memory
* Step 6: Tool Call Outputs
* Step 7: Structured Output
