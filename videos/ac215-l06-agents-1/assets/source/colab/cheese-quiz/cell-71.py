async def run_guild(topic: str) -> str:

    # seed the orchestrator with the user's topic
    prompt = f"Customer requests a quiz on: {topic}. Produce the final JSON."
    result = await Runner.run(
        orchestrator, prompt, max_turns=12
    )
    quiz = result.final_output
    html_str = render_quiz_html(quiz, shuffle_questions=False, shuffle_options=False)
    return HTML(html_str)
