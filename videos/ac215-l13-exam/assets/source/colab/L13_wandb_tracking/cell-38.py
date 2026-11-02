############################
# Training Params
############################
learning_rate = 0.01
initial_epoch = 0
epochs = 25

# Free up memory
K.clear_session()

# Optimizer
optimizer = keras.optimizers.SGD(learning_rate=learning_rate)
# Loss
loss = keras.losses.categorical_crossentropy

# Build or Load Model
model_name = "2_block"
if not LOAD_PREV_TRAINED:
  # Build the model
  model = build_2_block_model(image_height, image_width, num_channels, num_classes)

  # Print the model architecture
  print(model.summary())

  # Compile
  model.compile(loss=loss,
                    optimizer=optimizer,
                    metrics=['accuracy'])
else:
  # Load model
  model = keras.models.load_model(PREV_EXPERIMENT+"/"+model_name+".hdf5")
  with open(PREV_EXPERIMENT+"/"+model_name+"_train_history.json") as json_file:
    prev_training_history = json.load(json_file)
  with open(PREV_EXPERIMENT+"/"+model_name+"_model_metrics.json") as json_file:
    model_metrics = json.load(json_file)

  epochs = len(prev_training_history["loss"])
  initial_epoch=epochs
  epochs=epochs+3

# W&B
wandb.init(project='cheese-app-demo')
wandb.config = {
  "learning_rate": learning_rate,
  "epochs": epochs,
  "batch_size": batch_size,
  "model_name": model_name
}
wandb.run.name = model_name
wandb.run.save("test")


# Train model
start_time = time.time()
training_results = model.fit(
        train_data,
        validation_data=validation_data,
        epochs=epochs,
        initial_epoch=initial_epoch,
        callbacks=[WandbCallback(save_graph=False, save_model=False)],
        verbose=1)
execution_time = (time.time() - start_time)/60.0
print("Training execution time (mins)",execution_time)

# Get model training history
training_history = training_results.history

if LOAD_PREV_TRAINED:
  # Append previous training history & time
  training_history = append_training_history(training_results.history,prev_training_history)
  execution_time = model_metrics["execution_time"] + execution_time

# Save and custom model tracking
evaluate_save_model(model,test_data, training_history,execution_time, learning_rate, batch_size, epochs, optimizer,save=True)

# Update W&B
wandb.config.update({"execution_time": execution_time})