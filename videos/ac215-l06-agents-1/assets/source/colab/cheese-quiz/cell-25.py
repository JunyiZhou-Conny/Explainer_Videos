# Initialize
base_llm = BaseLLM(model)
reasoning_llm = ReasoningLLM(base_llm)

print("\n" + "="*50)
print("REASONING LLM:",model)
print("="*50)
reasoning_result = reasoning_llm.reason(user_prompt)
print(f"Final Response:")
display(Markdown(reasoning_result['response']))
print(f"Sub-questions explored: {len(reasoning_result['reasoning_steps']['sub_questions'])}")
print(f"Total tokens: {reasoning_result['total_tokens']}, Time: {reasoning_result['processing_time']:.2f}s")
