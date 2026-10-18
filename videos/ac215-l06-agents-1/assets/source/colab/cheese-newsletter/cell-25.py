# @title Orchestrator Agent

def build_orchestrator() -> Agent:
    # LLM
    MODEL_NAME = "gpt-5.6-luna"
    client = OpenAIChatClient(
        model=MODEL_NAME,
        function_invocation_configuration={"max_iterations": 16},
    )

    # Tools
    tools = [
        researcher_agent,
        editor_agent,
        send_email,
    ]

    # Agent
    agent = Agent(
        client=client,
        name="newsletter_orchestrator",
        instructions=ORCHESTRATOR_INSTRUCTIONS,
        tools=tools,
        # These tools mutate the same draft; run them sequentially.
        default_options={"allow_multiple_tool_calls": False},
    )

    return agent
