## <font color ='#16AD04'>**2. Learning Objectives** </font>

This guided tutorial covers:

- Understanding 4-bit quantization and its parameters (NF4, double quantization)
- Loading quantized versions of LLMs when resources are limited
- Configuring LoRA (Low-Rank Adaptation) for efficient fine-tuning
- Preparing and formatting datasets for instruction fine-tuning
- Fine-tuning a quantized model using QLoRA
- Evaluating and testing the fine-tuned model
- Saving LoRA adapters and merged models

## <font color ='#16AD04'>**Table of Contents** </font>

**Part A: Setup / Environment**
- Introduction to Quantization and QLoRA
- Environment setup and model pre-downloading
- Hugging Face authentication

**Part B: The 'Q' in QLoRA - Understanding 4-bit Quantization**
- Loading models in 4-bit precision
- Understanding quantization parameters (NF4, compute dtype, double quantization)
- Verifying and testing quantized models

**Part C: Fine-Tuning Qwen3 0.6B with QLoRA**
1. Loading the quantized Qwen3 model
2. Inspecting model parameters
3. Preparing the training dataset
4. Configuring LoRA and training arguments, Fine-tuning with SFTTrainer
5. Evaluating the fine-tuned model
6. Saving adapters and merged models