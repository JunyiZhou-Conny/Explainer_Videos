# Save trained model in our drive.
MODEL_NAME = "Qwen0.6B-finetune_cheese"
trainer.model.save_pretrained(os.path.join(cache_dir,MODEL_NAME))
# Save tokenizer
tokenizer.save_pretrained(os.path.join(cache_dir,MODEL_NAME))
