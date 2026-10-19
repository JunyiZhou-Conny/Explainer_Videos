# @title Step 4: Adding Short-term Memory
print("\n" + "="*70)
print("Step 4: With Conversation State/History (Short-term Memory)")
print("="*70)

system_prompt = """You are a culinary expert specializing in cheese and comfort foods.
When recommending cheeses, consider:
- Melting properties and optimal temperatures
- Flavor profiles (mild to sharp)
- Availability in typical grocery stores
- Practical cooking techniques

Be specific, practical, and explain your reasoning.

Remember the user's preferences and previous questions in this conversation"""

# Build conversation history
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "I'm cooking for my kids who prefer mild flavors"},
    {"role": "assistant", "content": "Great! I'll keep that in mind. Kids often prefer milder, creamier cheeses. What would you like to make?"},
    {"role": "user", "content": "Should I use butter or mayo on the bread?"},
    {"role": "assistant", "content": "For kids, I'd recommend butter on the outside of the bread - it creates a golden, crispy texture they'll love. Mayo works too and browns more evenly, but butter has a more familiar, comforting taste."},
    {"role": "user", "content": user_prompt}
]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0.2,
)

display(Markdown(response.choices[0].message.content))
