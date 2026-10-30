# Agent

store = Store()
request = load_scenario(SCENARIO)
print("👤 Customer ask:\n" + customer_ask(request))

async with AsyncOpenAI(timeout=45, max_retries=0) as api:
    client = OpenAIChatClient(
        model=MODEL,
        async_client=api,
        function_invocation_configuration=FUNCTION_LIMITS,
    )
    agent = Agent(
        client=client,
        name="FormaggioAssistant",
        instructions=instructions(store),
        tools=build_tools(store, request, None, None),
        default_options={**MODEL_OPTIONS, "response_format": AgentReply},
    )
    bare_response = await agent.run(customer_message(request))

display("\n💬 Agent's response:\n" + bare_response.value.message)
