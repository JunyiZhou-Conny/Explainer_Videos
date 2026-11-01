# def transform_conversation(example):
#     reformatted_segments = []
#     human_text = example['question']
#     assistant_text = example['answer']
#     # Qwen3 chat template format
#     reformatted_segments.append(f'<|im_start|>user\n{human_text}<|im_end|>\n<|im_start|>assistant\n{assistant_text}<|im_end|>')

#     return {'text': ''.join(reformatted_segments)}

def transform_conversation(example):
    messages = [{"role": "user", "content": example["question"]},
                {"role": "assistant", "content": example["answer"]}]
    return {"text": tokenizer.apply_chat_template(messages, tokenize=False).removesuffix("\n")}

dataset = dataset_df.map(transform_conversation)