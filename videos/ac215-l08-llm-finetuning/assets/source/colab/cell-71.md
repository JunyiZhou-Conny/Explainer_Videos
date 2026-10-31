### <font color ='#0376B9'>**4.3 Initialize the Supervised Fine-Tuning Trainer** </font>

The [SFTTrainer](https://huggingface.co/docs/trl/sft_trainer#trl.SFTTrainer) from the `trl` library handles the training loop.

`trl` stores the LoRA weights of a 4-bit model in bfloat16. We train with `fp16=True` so that the notebook also runs on T4 GPUs, and fp16 training needs those weights in float32, so the cell converts them after creating the trainer: