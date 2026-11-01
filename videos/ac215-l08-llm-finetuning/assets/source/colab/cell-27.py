# This will generate the output, as numerical tokens
outputs = model.generate(**inputs, max_new_tokens=20)
print(outputs)
# Using the decode method of the tokenizer, transform the output into natural language.
# The parameter skip_special_tokens=True will omit special tokens, such as <s> and </s>.
print(tokenizer.decode(outputs[0], skip_special_tokens=True))