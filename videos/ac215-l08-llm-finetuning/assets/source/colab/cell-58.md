### <font color ='#0376B9'>**3.5 Format for Qwen3 Chat Template** </font>

We let the tokenizer's chat template write Qwen3's special tokens (`<|im_start|>`, `<|im_end|>`). For a finished answer it also adds an empty `<think></think>` block, which is Qwen3's layout for answering without thinking. You can see it in 3.7.