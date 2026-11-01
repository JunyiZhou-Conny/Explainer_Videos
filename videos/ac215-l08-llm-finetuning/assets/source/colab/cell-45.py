text = "Hello my cheese name is"
device = "cuda:0"
inputs = tokenizer(text, return_tensors="pt").to(device)

outputs = base_model.generate(**inputs, max_new_tokens=20)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))