# Set supervised fine-tuning parameters
trainer = SFTTrainer(
    model=base_model,             # Model to be fine-tunned
    train_dataset=train_dataset,  # The dataset to train with
    peft_config=peft_config,      # LoRA configuration
    args=training_arguments,      # Trainig arguments defined before

)

# trl converts the LoRA weights of a 4-bit model to bfloat16. fp16 training (fp16=True above) cannot
# unscale bfloat16 gradients on the GPU, so keep the LoRA weights in float32.
for param in trainer.model.parameters():
    if param.requires_grad:
        param.data = param.data.float()

print_trainable_parameters(trainer.model)