# Print the number of parameters in the model
num_params = sum(p.numel() for p in base_model.parameters())
print(f"Number of parameters: {num_params/1000000} millions.")