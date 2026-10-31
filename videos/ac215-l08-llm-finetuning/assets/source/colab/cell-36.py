# Load Qwen tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name,
                                          max_length=512
                                          )
tokenizer.padding_side = "right"

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
                                                  model_name,
                                                  quantization_config=bnb_config,
                                                  device_map={"":0},
                                                  cache_dir=cache_dir
                                                )
# This function:
# 1. Freezes all base model parameters
# 2. Enables gradient checkpointing for memory efficiency
# 3. Sets up the model for k-bit training
base_model = prepare_model_for_kbit_training(base_model)