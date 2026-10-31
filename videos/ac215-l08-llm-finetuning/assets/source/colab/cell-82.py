# @title
# =============================================================================
# 🎯 SIMPLIFIED EVALUATION: Base vs Fine-Tuned Model Comparison
# =============================================================================

# -----------------------------------------------------------------------------
# STEP 1: Define Test Prompts
# -----------------------------------------------------------------------------
test_prompts = [
    "What are the key factors that differentiate between a 'fresh' cheese and an 'aged' cheese?",
    "What is the difference between 'Gorgonzola dolce' and 'Gorgonzola piccante', and how does the aging process affect the blue veins in each type?",
    "Why is the sky blue?",
]

# -----------------------------------------------------------------------------
# STEP 2: Helper Function for Generation
# -----------------------------------------------------------------------------

def generate_response(model, tokenizer, prompt, max_tokens=100,  enable_thinking=False):
    """Generate a response from the model"""
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=enable_thinking
    )

    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        # temperature=0.0,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id
    )

    # response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # # Extract only the assistant's response
    # return response.split("assistant\n")[-1].strip()

    new_tokens = outputs[0][inputs["input_ids"].shape[1]:]   # drop the prompt
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


print("✅ Helper function ready!")

# -----------------------------------------------------------------------------
# STEP 3: Load Base Model (Without LoRA) for comparison
# -----------------------------------------------------------------------------

print("Loading base model for comparison...")

base_model_comparison = AutoModelForCausalLM.from_pretrained(
    model_name,
    # quantization_config=bnb_config,
    dtype=torch.float16,
    device_map="auto",
    cache_dir=cache_dir
)

print("✅ Base model loaded!")

# -----------------------------------------------------------------------------
# STEP 4: Run Comparison
# -----------------------------------------------------------------------------

print("\n" + "="*80)
print("🚀 COMPARING BASE vs FINE-TUNED MODEL")
print("="*80)

for i, prompt in enumerate(test_prompts, 1):
    print(f"\n📝 Test {i}/{len(test_prompts)}: {prompt}")
    print("-"*80)

    # Get base model response
    print("🔵 Generating base model response...")
    base_response = generate_response(base_model_comparison, tokenizer, prompt)

    # Get fine-tuned model response (your trained model)
    print("🟢 Generating fine-tuned model response...")
    finetuned_response = generate_response(base_model, tokenizer, prompt) # base_model is the fine-tuned model here

    # Display side-by-side
    html = f"""
    <div style="border: 2px solid #666; padding: 15px; margin: 10px 0; border-radius: 8px; background-color: rgba(128, 128, 128, 0.1);">
        <div style="background-color: rgba(255, 152, 0, 0.15); border-left: 4px solid #FF9800; padding: 12px; margin-bottom: 15px; border-radius: 5px;">
            <strong style="color: #FF9800; font-size: 15px;">📝 Prompt:</strong>
            <div style="margin-top: 5px; font-size: 14px; line-height: 1.5;">{prompt}</div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div style="background-color: rgba(33, 150, 243, 0.1); border-left: 4px solid #2196F3; padding: 12px; border-radius: 5px;">
                <strong style="color: #2196F3; font-size: 15px;">🔵 Base Model:</strong>
                <div style="margin-top: 8px; line-height: 1.6; font-size: 14px;">{base_response}</div>
            </div>
            <div style="background-color: rgba(76, 175, 80, 0.1); border-left: 4px solid #4CAF50; padding: 12px; border-radius: 5px;">
                <strong style="color: #4CAF50; font-size: 15px;">🟢 Fine-Tuned Model:</strong>
                <div style="margin-top: 8px; line-height: 1.6; font-size: 14px;">{finetuned_response}</div>
            </div>
        </div>
    </div>
    """
    display(HTML(html))

print("\n" + "="*80)
print("✅ EVALUATION COMPLETE!")
print("="*80)