orchestrator = Agent(
    name="Cheese Quiz Guild Orchestrator",
    instructions=(
        "Act as the head of the Cheese Quiz Guild. "
        "Follow the assembly line strictly:\n"
        "1) Call research_facts(topic). If the topic is vegan/plant-based, also call vegan_specialist.\n"
        "   Merge/trim to ~5 total facts (no duplicates), and update context.fact_cache[topic].\n"
        "2) Call write_quiz(topic, facts).\n"
        "3) Call review_quiz(draft, facts). If not approved and not needs_user_opinion, "
        "   send exactly one revision request back to write_quiz and then re-review. "
        "   (Make at most 2 total review rounds.)\n"
        "   If needs_user_opinion, call ask_head_cheesemonger to decide and proceed.\n"
        "4) format_quiz_json(approved_draft) → JSON.\n"
        "Keep outputs structured between steps; only the last step returns JSON."
    ),
    tools=[
        stilton_tool,
        cashew_tool,
        brie_tool,
        cheddar_tool,
        ricotta_tool,
        ask_head_cheesemonger,
    ],
    output_type=QuizAgentOutputSchema(),
    model_settings=ModelSettings(),
)
