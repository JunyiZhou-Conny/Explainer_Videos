# @title Step 7: Structured Output
print("\n" + "="*70)
print("Step 7: With Structured Output")
print("="*70)

# 🔒 JSON Schema for strict output
schema = {
    "type": "object",
    "properties": {
        "top_recommendation": {"type": "string"},
        "alternatives": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1
        },
        "cooking_tips": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1
        },
        "why_this_works": {"type": "string"}
    },
    "required": ["top_recommendation", "alternatives", "cooking_tips", "why_this_works"],
    "additionalProperties": False
}

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": enhanced_user_prompt}
    ],
    # ✅ Structured Outputs with strict JSON Schema
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "CheeseAdvice",
            "strict": True,          # guarantees valid JSON and schema adherence
            "schema": schema
        }
    },
    temperature=0.2,
)

# The model returns a JSON string in message.content
raw_json = response.choices[0].message.content
data = json.loads(raw_json)

# Pretty print as fenced JSON (or use it programmatically)
display(Markdown(f"```json\n{json.dumps(data, indent=2)}\n```"))
