# Reload model in FP16 and merge it with LoRA weights
base_model = AutoModelForCausalLM.from_pretrained(
    model_name,
    dtype=torch.float16,
    device_map={"":0},
    cache_dir=cache_dir
  )
# Now, configure the LoRA weights to the base_model
model = PeftModel.from_pretrained(base_model, os.path.join(cache_dir,MODEL_NAME))
# This line applies the merging operation. We re-write the PEFT model.
model = model.merge_and_unload()

# Reload tokenizer to save it
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"


# Save trained model in our drive.
model.save_pretrained(os.path.join(cache_dir,f"{MODEL_NAME}_merged"))
# Save tokenizer
tokenizer.save_pretrained(os.path.join(cache_dir,f"{MODEL_NAME}_merged"))