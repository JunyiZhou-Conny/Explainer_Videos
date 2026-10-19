LLMs are stateless functions. To get the best results, you need to give LLMs the best inputs. Managing LLM inputs (context) is about building:
* The instructions you give to the model. The system prompt & user prompt
* Any documents or external data you retrieve (e.g. RAG)
* Any tool call output
* Any past state or other history (Short-term Memory)
* Any past messages or events from related but separate histories/conversations (Long-term Memory)
* Instructions about what sorts of structured data to output

***Think of model context as the invisible layer that feeds and connects all parts of the agent.***

It manages what information the LLM sees, when it sees it, and how it uses it.
Without the right context, even the best reasoning model cannot plan, adapt, or remember effectively.
