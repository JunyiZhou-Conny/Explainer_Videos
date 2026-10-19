# Initialize
agent = SimpleAgent(model)

print("\n" + "="*50)
print("AGENT:",model)
print("="*50)
agent_result = await agent.generate(user_prompt)
print(f"Final Response:")
display(Markdown(agent_result['response']))
print(f"Tools used: {len(agent_result['tools'])}")
print(f"Time: {agent_result['processing_time']:.2f}s")
