# @title Start an interactive conversation
async def read_interactive_message() -> str:
    """Read one possibly multiline message, terminated by blank line or /send."""
    lines: list[str] = []
    while True:
        label = "You: " if not lines else "...  "
        try:
            line = await asyncio.to_thread(input, label)
        except EOFError:
            if lines:
                return "\n".join(lines).strip()
            raise

        command = line.strip().casefold()
        if not lines and command in {"exit", "quit"}:
            return command
        if command == "/send" or not line.strip():
            if lines:
                return "\n".join(lines).strip()
            continue
        lines.append(line)

async def chat_loop():
    # Build the Agent
    agent, session, context = build_agent()

    print("Travel Planner (interactive). Enter one or more lines, then use a blank")
    print("line or /send to submit. Commands: 'exit' or 'quit' to leave.\n")

    try:
        while True:
            try:
                # Read input off the event loop so we don't block it. Buffering
                # lines prevents a pasted paragraph from becoming several turns.
                prompt = await read_interactive_message()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break

            if not prompt:
                continue
            if prompt.casefold() in {"exit", "quit"}:
                print("Goodbye!")
                break

            try:
                await run_turn(agent, prompt, session, context, invoke_agent)
            except Exception as e:
                # Keep the session alive on a bad turn instead of crashing the demo.
                print(f"[error] {type(e).__name__}: {e}\n")
    finally:
        session.close()
