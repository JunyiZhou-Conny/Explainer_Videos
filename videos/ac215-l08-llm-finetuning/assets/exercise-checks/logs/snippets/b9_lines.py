GCS_BUCKET_NAME = os.environ["GCS_BUCKET_NAME"]
TRAIN_DATASET = f"gs://{GCS_BUCKET_NAME}/llm-finetune-dataset-small/train.jsonl"
VALIDATION_DATASET = f"gs://{GCS_BUCKET_NAME}/llm-finetune-dataset-small/test.jsonl"
