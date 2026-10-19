# Brie, the Creative Wordsmith
brie_agent = Agent(
    name="Brie, the Creative Wordsmith",
    model="gpt-4o",
    handoff_description="Writes engaging multiple-choice questions from facts.",
    instructions=(
        "Turn the given facts into exactly 5 multiple-choice questions. Each has 4 options (keys a,b,c,d) "
        "with one correct answer. Make them fun but precise; avoid trickiness; include source_note if present. "
        "Return ONLY structured QuizDraft."
    ),
    output_type=QuizDraft,
    model_settings=ModelSettings(temperature=0.7),
)

# Test
input = "Facts:\n" + "\n".join(f"- {f.statement}" for f in cheese_facts)
result = await Runner.run(brie_agent, input=input)
quiz_draft = result.final_output
display(quiz_draft)
