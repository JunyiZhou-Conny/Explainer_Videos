# Initialize
base_llm = BaseLLM(model)
llm_result = base_llm.generate(user_prompt)

print("\n" + "="*50)
print("BASE LLM:",model)
print("="*50)
print(f"Response:")
display(Markdown(llm_result['content']))
print(f"Tokens: {llm_result['tokens_used']}, Time: {llm_result['response_time']:.2f}s")
