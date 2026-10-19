# @title Step 2: Prompt Engineering
print("\n" + "="*70)
print("Step 2: With Prompt Engineering")
print("="*70)

# Well-crafted system prompt
system_prompt = """You are a culinary expert specializing in cheese and comfort foods.
When recommending cheeses, consider:
- Melting properties and optimal temperatures
- Flavor profiles (mild to sharp)
- Availability in typical grocery stores
- Practical cooking techniques

Be specific, practical, and explain your reasoning."""

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "user", "content": system_prompt},
        {"role": "system", "content": user_prompt}
    ],
    temperature=0.2,
)

display(Markdown(response.choices[0].message.content))
