# Load LoRA configuration
peft_config = LoraConfig(lora_alpha=16, # The LoRA scaling parameter
                        lora_dropout=0.1, # Dropoput probability in the LoRa layers
                        r=8, # Rank of the LoRA
                        bias="none", # Do not update any bias
                        task_type="CAUSAL_LM", # Type of model to train
                    )