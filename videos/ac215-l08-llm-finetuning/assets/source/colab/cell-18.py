# Here, we'll use the small facebook/opt-350m model as a toy example
# to understand exactly how 4-bit quantization works.
model_id = "facebook/opt-350m"

# To load the model in 4-bit, we need a special configuration.
# The BitsAndBytesConfig allows us to specify exactly how the quantization should be done.
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,                  # This is the magic flag that enables 4-bit loading.
    bnb_4bit_quant_type="nf4",          # We use "nf4" (Normal Float 4) for higher precision than the default.
    bnb_4bit_use_double_quant=True,     # We apply a second quantization step to save even more memory.
    bnb_4bit_compute_dtype=torch.float16 # This sets the data type for calculations (like matrix multiplications).
)

# Now, we load the tokenizer and the model with our quantization configuration.
tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir = cache_dir)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
    cache_dir=cache_dir
)