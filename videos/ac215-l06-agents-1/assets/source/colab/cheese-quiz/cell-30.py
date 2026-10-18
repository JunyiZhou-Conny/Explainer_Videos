# @title Define SimpleAgent
class SimpleAgent:
    """Demonstrates agent functionality - LLM, instructions, tool usage (research-oriented)"""

    def __init__(
        self,
        model: str = "gpt-4o",
        user_location: Dict[str, Any] | None = None,
        search_context_size: str = "medium",          # "low" | "medium" | "high"
        instructions: str | None = None,
    ):
        # Configure the web search tool
        web_tool = WebSearchTool(
            user_location=user_location,
            search_context_size=search_context_size
        )

        # Instructions similar to Reasoning LLM
        if instructions is None:
            instructions = (
                "You are a meticulous research agent. "
                "Before answering, outline a brief plan with 3–4 sub-questions. "
                "Use the web_search tool for up-to-date or factual details. "
                "Perform at least TWO web_search calls across DIFFERENT reputable domains. "
                "Cross-check key facts (dates, figures, definitions). "
                "Then write a clear, structured answer with sections and practical recommendations. "
                "Finish with a 'Sources' list (title + URL) covering the items you used."
            )

        self.agent = Agent(
            name="SimpleAgent",
            instructions=instructions,
            model=model,
            tools=[web_tool],
        )

    def _research_prompt(self, query: str) -> str:
        return f"""
Task: Answer the user's question comprehensively.

User question: {query}

Workflow you must follow:
1) **Plan**: List 3–4 concise sub-questions you will answer.
2) **Research**: Use `web_search` at least twice across different domains to gather facts.
3) **Synthesize**: Combine findings into a cohesive answer that is better than a generic LLM response.
4) **Verify**: Re-check critical claims and resolve conflicts if sources disagree.
5) **Present**: Write the final answer with these sections:
   - Summary (2–4 sentences)
   - Key Criteria / How to Choose
   - Top Recommendations (with brief justifications)
   - Smart Variations or Blends (if applicable)
   - Practical Tips (actionable steps)
   - Sources (bullet list: Title — URL)

Output format: Markdown.
If uncertainty remains, say what is uncertain and why.
"""

    async def generate(self, query: str) -> Dict[str, Any]:
        print(f"\n🤖 SimpleAgent: Running with web_search for '{query}'")
        start = time.time()

        # 🔧 pass the guided research prompt
        result = await Runner.run(self.agent, input=self._research_prompt(query))

        end = time.time()
        return {
            "response": result.final_output,
            "processing_time": end - start,
            "tools": self.agent.tools  # available tools (actual usage will show in logs/tracing if enabled)
        }
