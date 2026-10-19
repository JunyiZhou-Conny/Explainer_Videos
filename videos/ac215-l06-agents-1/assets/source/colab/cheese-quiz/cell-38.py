# @title Step 1: Basic prompt
print("\n" + "="*70)
print("Step 1: Basic Prompt")
print("="*70)

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.2,
)

display(Markdown(response.choices[0].message.content))
