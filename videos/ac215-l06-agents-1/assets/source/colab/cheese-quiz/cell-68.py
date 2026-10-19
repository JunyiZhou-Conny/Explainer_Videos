# Agents-as-tools for orchestration
stilton_tool = stilton_agent.as_tool(
    "research_facts", "Find ~5 concise, citable facts for a topic."
)
brie_tool = brie_agent.as_tool("write_quiz", "Convert facts into a 5-question MCQ quiz.")
cheddar_tool = cheddar_agent.as_tool("review_quiz", "QA the quiz against the facts.")
mozzarella_tool = mozzarella_agent.as_tool("format_quiz", "Format quiz into Markdown.")
ricotta_tool = ricotta_agent.as_tool("format_quiz_json", "Format quiz into JSON.")
cashew_tool = cashew_agent.as_tool(
    "vegan_specialist", "Supplement with vegan cheese facts as needed."
)
