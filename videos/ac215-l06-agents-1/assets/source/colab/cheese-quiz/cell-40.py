# @title Step 3: Retrieve Relevant Documents (e.g. RAG)
# Simulated knowledge base (in real apps, this would come from a vector database)
CHEESE_KNOWLEDGE_BASE = {
    "american_cheese": {
        "melting_temp": "150°F",
        "properties": "Smooth melt, mild flavor, contains emulsifiers for perfect texture",
        "best_for": "Classic grilled cheese, kids' sandwiches"
    },
    "cheddar": {
        "melting_temp": "170°F",
        "properties": "Rich flavor, can separate if overheated, varies by age",
        "best_for": "Flavor-focused sandwiches, adults"
    },
    "gruyere": {
        "melting_temp": "170°F",
        "properties": "Nutty and complex, excellent melt, slightly sweet",
        "best_for": "Gourmet grilled cheese, French onion soup"
    }
}

print("\n" + "="*70)
print("Step 3: With RAG (Retrieved Knowledge)")
print("="*70)

# System prompt
system_prompt = """You are a culinary expert specializing in cheese and comfort foods.
When recommending cheeses, consider:
- Melting properties and optimal temperatures
- Flavor profiles (mild to sharp)
- Availability in typical grocery stores
- Practical cooking techniques

Be specific, practical, and explain your reasoning."""

# Inject retrieved knowledge into the prompt
enhanced_user_prompt = f"""Based on this cheese data:
{str(CHEESE_KNOWLEDGE_BASE)}
User question: {user_prompt}"""

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": enhanced_user_prompt}
    ],
    temperature=0.2,
)

display(Markdown(response.choices[0].message.content))
