# Cheddar, the Sharp Critic
cheddar_agent = Agent(
    name="Cheddar, the Sharp Critic",
    handoff_description="Reviews quiz clarity & correctness vs facts; requests fixes.",
    instructions=(
        "Compare each question to the supplied facts. Flag ambiguous, too-easy/too-hard, or ungrounded items. "
        "Use ensure_unique_answers to detect duplicate options. If borderline difficulty or taste-based, "
        "set needs_user_opinion=True. Produce ReviewResult with indices & notes."
    ),
    tools=[ensure_unique_answers, ask_head_cheesemonger],
    output_type=ReviewResult,
    model_settings=ModelSettings(temperature=0.2),
)

# Mozzarella, the Master Formatter
mozzarella_agent = Agent(
    name="Mozzarella, the Master Formatter",
    handoff_description="Formats the approved quiz for delivery.",
    instructions=(
        "Format the final, approved QuizDraft into Markdown:\n"
        "• Title\n• Numbered questions\n• Lettered options (a–d)\n• **Answer Key**\n• Optional sources."
    ),
    output_type=str,
    model_settings=ModelSettings(temperature=0.2),
)

# Cashew Agent, Dynamic specialist
cashew_agent = Agent(
    name="Cashew, the Plant-Based Pro",
    handoff_description="Adds vegan/plant-based cheese expertise to research.",
    instructions=(
        "Augment Stilton with up to 3 extra facts when the topic includes vegan/plant-based."
    ),
    tools=[WebSearchTool()],
    output_type=List[CheeseFact],
    model_settings=ModelSettings(temperature=0.4),
)

# Ricotta Agent
ricotta_agent = Agent(
    name="Ricotta, the Schema Scribe",
    handoff_description="Converts an approved quiz into strict JSON that matches the provided schema.",
    instructions=(
        "You will receive an approved quiz (questions with options and the correct answer). "
        "Output ONLY valid JSON that conforms to the provided schema. No markdown, no comments.\n"
        "RULES:\n"
        "1) Output ONLY raw JSON (no Markdown fences, no commentary).\n"
        "2) Use sequential integer IDs starting at 1.\n"
        "3) Each question MUST have exactly four options with 'letter' keys: 'a', 'b', 'c', 'd'.\n"
        "4) The 'answer' must equal one of the option letters ('a'|'b'|'c'|'d').\n"
        "5) Preserve the original question wording and option texts; do not invent facts.\n"
        "6) Do not include sources or extra fields—only the fields in the schema.\n"
    ),
    output_type=QuizAgentOutputSchema(),  # <- custom schema object
    model_settings=ModelSettings(temperature=0.1),
)
