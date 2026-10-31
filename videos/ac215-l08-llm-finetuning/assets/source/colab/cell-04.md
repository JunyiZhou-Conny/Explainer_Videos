In this notebook, we will demonstrate how to fine-tune the [Qwen 3 model](https://qwen.ai/blog?id=1e3fa5c2d4662af2855586055ad037ed9e555125&from=research.research-list) using QLoRA and `bitsandbytes` with `PyTorch` (HuggingFace).

QLoRA is a technique that leverages quantized low-rank adaptation to make the fine-tuning process more efficient.


The `bitsandbytes` integration which includes the work from the [QLoRA paper](https://arxiv.org/abs/2305.14314) and provides us with the capability to load models with 4-bit quantization with little loss in quality.

Considering the limitation of resources when accessing large open source models, this allows a much wider audience access to LLM inference and training.

In summary:
- **4‑bit quantization**: Cuts memory usage substantially while preserving most of the model's quality.
- **Low‑rank adapters**: Only a small set of parameters are trained and saved.
- **Hugging Face ecosystem**: Works seamlessly with common training utilities.
- **Versatile**: Applicable to text and vision-language models (e.g., [Qwen3-VL](https://huggingface.co/collections/Qwen/qwen3-vl); every [Qwen3.5](https://qwen.ai/blog?id=qwen3.5) model also accepts images).


