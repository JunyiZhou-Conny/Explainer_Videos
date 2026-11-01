# <font color ='#16AD04'>**Part C: Fine-Tuning Qwen3 0.6B with QLoRA** </font>

Now that we understand the 'Q' (Quantization) from Part B, let's bring in the 'LoRA' (Low-Rank Adaptation) and fine-tune our target model, `Qwen/Qwen3-0.6B`. We will load this model in 4-bit and then train it on a custom dataset.

### <font color ='#16AD04'>**About the Qwen Model Family** </font>

[Qwen (通义千问)](https://qwen.ai/) is a family of large language models developed by Alibaba Cloud's research team in China. The Qwen ecosystem has grown to hundreds of models across text, vision, speech, embedding and code, in many sizes.


### <font color ='#16AD04'>**Loading the Quantized Qwen3 Model** </font>

We can even load a massive 20-billion parameter model (which would normally require 40GB in half precision) entirely on a GPU using this method!

You can try `model_id = "EleutherAI/gpt-neox-20b"` later.

For now, we'll use NF4 quantization for better storage performance, `float16` for the compute data type, and double quantization to optimize memory usage during model loading.