

## <font color ='#16AD04'>**3. Deeper Dive: 4-bit Quantization Parameters** </font>
### <font color ='#0376B9'>**Changing the Compute dtype** </font>

Adjusting `compute_dtype` can enhance model computation speed and memory efficiency by using lower precision formats like `bf16` instead of the default `float32`.

<details>
  <summary>Click here for more details</summary>

  - The **compute dtype** determines the data type used for internal calculations within the model. For example, while the model's parameters might be stored in `4bitNormalFloat`, computations can be performed using `bf16` (16-bit brain floats) to improve precision.
   - Using a lower-precision dtype like bf16 can reduce memory usage and sometimes make computations faster, depending on the hardware. This is especially beneficial for large models.
  - By default, the compute dtype is set to `float32` to maintain standard precision.

</details>

### <font color ='#0376B9'>**Changing the Quantization Type** </font>

Switch between FP4 and NF4 4-bit quantization types for evaluation using the `bnb_4bit_quant_type`.

<details>

  <summary>Click here for more details</summary>

  - The 4-bit quantization integration includes two types: **FP4** and **NF4**.
  - **FP4** is a standard 4-bit floating point representation.
  - **NF4** (Normal Float 4) is a more specialized 4-bit format introduced in the [QLoRA paper](https://arxiv.org/abs/2305.14314), which can offer better accuracy compared to FP4 for certain models. See lecture notes for explanation.
  - You can switch between FP4 and NF4 using the `bnb_4bit_quant_type` parameter in `BitsAndBytesConfig`. By default, FP4 is used.


</details>

### <font color ='#0376B9'>**Using Double Quantization for More Memory Efficient Inference and Training** </font>

Enable double quantization with `bnb_4bit_use_double_quant=True` to significantly reduce memory usage, allowing large models to run on less powerful hardware.

<details>
  <summary>Click here for more details</summary>

  - **Double quantization** is a technique that organizes the quantized parameters in a way that further reduces memory usage without degrading the performance.
  - Sometimes called nested quantisation.
  - This method is particularly useful when working with very large models, as it enables running them on hardware with limited memory.
  - For example, double quantization allows fine-tuning a large model like llama-13b on a relatively small GPU (NVIDIA-T4 16GB), supporting longer sequence lengths and more gradient accumulation steps.
  - To enable double quantization, include `bnb_4bit_use_double_quant=True` in your quantization configuration.
  See extra slides in lecture notes.
</details>

### <font color ='#0376B9'>**Combining All the Features Together** </font>

Combine quantization types, double quantization, and compute dtype settings to optimize model performance and efficiency on limited hardware.

<details>
  <summary>Click here for more details</summary>

  - These features are not mutually exclusive and can be used together to optimize model performance and efficiency.
  - For instance, you can configure a model to use `nf4` for quantization, enable double quantization to save memory, and set the compute dtype to `bfloat16`.
  - Combining these features can lead to significant improvements in how efficiently a model runs, especially on limited hardware.

</details>

---