# @title Step 6: Tool Call Outputs
print("\n" + "="*70)
print("Step 6: With Tool Call Outputs")
print("="*70)

# Simulated tool functions: Results from function calls (APIs, databases, calculations)
check_grocery_inventory = {
    "Kraft American Singles": {"price": 4.99, "in_stock": True},
    "Whole Foods Mild Cheddar": {"price": 13.49, "in_stock": True},
    "Tillamook Medium Cheddar": {"price": 55.99, "in_stock": True},
    "Boar's Head Vermont Cheddar": {"price": 8.99, "in_stock": False}
}
check_lactose_content = {
    "american": {"lactose_per_slice": "0.1g", "note": "processed, lactose removed"},
    "mild_cheddar": {"lactose_per_slice": "0.2g", "note": "naturally low"},
    "aged_cheddar": {"lactose_per_slice": "0.1g", "note": "aging reduces lactose"}
}
simulate_melting = {
    "american": "Smooth melt, no separation, kid-friendly texture",
    "mild_cheddar": "Good melt, slight oil separation at high heat, richer flavor"
}

# Format tool outputs for context
tool_outputs = f"""Tool Call Results:

Grocery Inventory at Whole Foods:
{str(check_grocery_inventory)}

Lactose Content Analysis:
{str(check_lactose_content)}

Melting Simulation Results:
{str(simulate_melting)}"""

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

# Inject tool outputs into the prompt
enhanced_user_prompt = f"""{str(tool_outputs)}
Use this real-time data to make your recommendation.
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
