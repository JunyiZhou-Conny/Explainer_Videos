# **Part B - The 'Q' in QLoRA - Understanding 4-bit Quantization**

<img src="https://drive.google.com/uc?export=view&id=10pb7_J91RdkM-zV9Kgxo65iYHtqgoQ9Q" width="500">

Ref: [Image Source](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-quantization)


Notes:
- Imagine that the original model weights are stored as high-precision 32-bit (or 16) numbers, which can fall anywhere along this smooth curve. There are billions of possible values.
- Quantization is the process of sorting all of these values into a small, fixed number of buckets. In our case, since we're using 4-bit quantization, we only have 16 possible buckets to put them in.
- As you can see, we take the original value and find the closest bucket to represent it. This is how we go from a large FP32 model to a much smaller 4-bit model. We've simplified the numbers.

## <font color ='#16AD04'>**Loading Models in 4-bit** </font>

To demonstrate 4-bit quantization practically, we will use a manageable, GPT-like model: ["OPT-350m - OPT : Open Pre-trained Transformer Language Models](https://huggingface.co/facebook/opt-350m)"

To load this model in 4-bit, we cannot use the standard loading process. If we loaded it normally, it would use standard 32-bit or 16-bit precision. Instead, we must:

- Define a `BitsAndBytesConfig`: This object specifies exactly how we want to perform the quantization (e.g., which 4-bit data type to use).
- Pass this configuration to `AutoModelForCausalLM`.from_pretrained: We use the quantization_config argument to tell the transformers library to compress the model on-the-fly as it loads it into the GPU.
The following cell performs these steps.
