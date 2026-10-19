# Professor Stilton, the Fact-Finder
stilton_agent = Agent(
    name="Professor Stilton, the Fact-Finder",
    model="gpt-4o",
    handoff_description="Gathers concise, citable cheese facts for a topic.",
    instructions=(
        "You are Professor Stilton. Given a cheese topic, use web search to gather ~5 concise, "
        "verifiable facts suitable for quiz questions. Include short source notes (domain or title). "
    ),
    tools=[WebSearchTool()],
    output_type=List[CheeseFact],
    model_settings=ModelSettings(temperature=0.3, tool_choice="auto"),
)

# Test
result = await Runner.run(stilton_agent, "Cheese topic: brie")
cheese_facts = result.final_output
for fact in cheese_facts:
    print(f"{fact.statement} ({fact.source})")
