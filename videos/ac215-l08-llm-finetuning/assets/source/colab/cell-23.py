text = "Hello my cheese name is"
device = "cuda:0"

inputs = tokenizer(text, return_tensors="pt").to(device)