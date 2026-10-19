# expected (README text, not program output): dlops-io/llm-rag, main @ e17a39f35bc07b440f573def480adaf4703f8b91, README.md:261-271 (section "Agents"), unchanged. The README prints no output for --agent; this is its own description of the step and the link to the hosted tool.
This will:

- Take the user question and pass it to LLM to find the user intent (e.g: `Describe where cheese making is important in Pavlos's book?`)
- Perform function calling to get all the responses required to answer the question
- Pass the query and context to the LLM
- Displays the LLM's response

To test out the Cheese Agent, you can use this [Cheese Agent Tool](https://ac215-llm-rag.dlops.io/agent).

> [!NOTE]
> Use Chrome browser for best performance.
