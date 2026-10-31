
### <font color ='#0376B9'>**5.1 Quantitative Evaluation: Loss and Perplexity** </font>

Before testing qualitative generation, let's evaluate the model quantitatively on our test set:

- **Loss**: Measures how well the model predicts the next token (lower is better)
- **Perplexity**: Exponential of loss, represents the model's "confusion" (lower is better)
  - Perplexity of 10 means the model is as confused as if it had to choose uniformly among 10 options
  - Perplexity = exp(loss)

We score two models on the same 100 test examples: the **base model** (the same 4-bit model with its LoRA adapter switched off) and the **fine-tuned model**. The difference between them shows what fine-tuning changed. The loss covers every token of each example, including the question and the chat-template tokens, not only the answer.
