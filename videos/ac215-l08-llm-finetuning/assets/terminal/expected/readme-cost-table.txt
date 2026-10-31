# expected: README.md:267-278 of dlops-io/llm-finetuning @ 44ef6f0 (main): Cost of Fine-tuning (Gemini 1.5 Flash pricing, 3 epochs; the code now tunes gemini-3.1-flash-lite for 1 epoch, see digest E6). Documented by the tutorial, not produced here. Names masked (‹instructor›).
Cost of fine-tuning model on Agent Platform (formerly Vertex AI):

Gemini 1.5 Flash Tuning is 0.008 USD per 1,000 tokens. The below table shows examples of how much it would cost as you have more documents

| Tokens    | Epochs | Total Tokens | Price per 1000 | Cost    | # Documents |
|-----------|--------|--------------|----------------|---------|-------------|
| 4,697,472 | 3      | 14,092,416   | $0.008         | $112.73 | 16,444 ***  |
| 23,874    | 3      | 71,622       | $0.008         | $0.573  | 88          |

*** Way too much data for this fine tuning!

Refer to Agent Platform Pricing for various tasks at their [pricing page](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing).
