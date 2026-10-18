# @title Step 5: Adding Long-term Memory
print("\n" + "="*70)
print("Step 5: With Long-term Memory (Past Sessions)")
print("="*70)

# Information from past conversations (assume stored in a database)
USER_MEMORY = {
    "user_id": "user_123",
    "preferences": {
        "previous_cheese_choice": "mild cheddar (mac and cheese, 2 weeks ago)",
        "dietary_restrictions": "lactose sensitivity",
        "shopping_location": "Whole Foods",
        "budget_preference": "under $20",
        "household": "cooking for kids",
        "health_preference": "Prioritize health-conscious choices; consider portion size, sodium, and saturated fat.",
        "ingredient_preference": (
            "Only recommend cheeses with simple, natural ingredients such as milk, cultures, salt, and enzymes/rennet. "
            "Avoid artificial colors, artificial flavors, artificial preservatives, and processed cheese products with added emulsifying salts. "
            "Check the actual ingredient list; if it is unavailable, do not assume the product meets this preference. "
            "Ingredient requirements take priority over price or melting performance. Do not equate natural ingredients with automatically being healthier."
        )
    }
}

# Load user memory
memory_context = f"""User Profile:
- Previously enjoyed: {USER_MEMORY['preferences']['previous_cheese_choice']}
- Dietary note: {USER_MEMORY['preferences']['dietary_restrictions']}
- Shops at: {USER_MEMORY['preferences']['shopping_location']}
- Budget: {USER_MEMORY['preferences']['budget_preference']}
- Household: {USER_MEMORY['preferences']['household']}
- Health priorities: {USER_MEMORY['preferences']['health_preference']}
- Ingredient requirements: {USER_MEMORY['preferences']['ingredient_preference']}"""

# System prompt
system_prompt = f"""You are a culinary expert specializing in cheese and comfort foods.
When recommending cheeses, consider:
- Melting properties and optimal temperatures
- Flavor profiles (mild to sharp)
- Availability in typical grocery stores
- Practical cooking techniques

Be specific, practical, and explain your reasoning.

{memory_context}

Use this information to personalize your recommendations."""

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "I'm cooking for my kids who prefer mild flavors"},
    {"role": "assistant", "content": "Great! I'll keep that in mind. Kids often prefer milder, creamier cheeses. What would you like to make?"},
    {"role": "user", "content": user_prompt}
]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0.2,
)
display(Markdown(response.choices[0].message.content))
