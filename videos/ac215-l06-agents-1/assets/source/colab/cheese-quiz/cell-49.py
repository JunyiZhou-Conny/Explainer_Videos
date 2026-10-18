# System Prompt
system_prompt = """You are a culinary expert specializing in cheese and comfort foods.
When recommending cheeses, consider:
- Melting properties and optimal temperatures
- Flavor profiles (mild to sharp)
- Availability in typical grocery stores
- Practical cooking techniques

Be specific, practical, and explain your reasoning.

Call the pavlos_fun_fact_tool tool 2–3 times and add facts to your response."""

# Build an agent that uses "pavlos_fun_fact_tool"
culinary_expert_agent = Agent(
    name="Culinary Expert",
    instructions=system_prompt,
    model=model,
    tools=[pavlos_fun_fact_tool],
    model_settings=ModelSettings(temperature=0.2),
)

print("\n" + "="*50)
print("Culinary Expert Agent (with fun facts tool call):",model)
print("="*50)
agent_result = await Runner.run(culinary_expert_agent, input=user_prompt)
print(f"Final Response:")
display(Markdown(agent_result.final_output))
