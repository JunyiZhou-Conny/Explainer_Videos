# Set training parameters
training_arguments = SFTConfig(
    max_length=512,
    output_dir= "./results",       # Directory to store the results
    num_train_epochs=2,            # Number of epochs to train
    per_device_train_batch_size=4, # Batch size for each GPU
    optim="paged_adamw_32bit",     # Optimizer to use
    save_strategy="no",            # Do not write checkpoints during training; Step 6 saves the adapters.
    logging_steps=50,              # Number of steps between logs
    learning_rate=2e-4,            # Learning rate of the optimizer
    weight_decay=0.01,             # Weight decay to apply during optimization
    fp16=True,                    # Uses float16 instead of float32
    bf16=False,                     # Uses bfloat16 instead of float32
    max_grad_norm=1,               # Maximum gradient norm for gradient clipping
    train_sampling_strategy="group_by_length",  # Batches sequences of similar length together to reduce padding
    lr_scheduler_type="cosine",    # Scheduler to apply to the learning rate
    report_to="tensorboard",        # Format in which to store the logs
)

