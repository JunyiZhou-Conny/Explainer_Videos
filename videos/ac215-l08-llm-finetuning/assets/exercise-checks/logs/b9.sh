# B9 and C5: module-level os.environ[...] lookups run on import, even for --help.
cd /repo/gemini-finetuner
step 'python cli.py --help | head -1'
step 'env -u GCP_PROJECT python cli.py --help 2>&1 | tail -4'
step "sed -i '10,11d' cli.py && sed -i '9a GCS_BUCKET_NAME = os.environ[\"GCS_BUCKET_NAME\"]\nTRAIN_DATASET = f\"gs://{GCS_BUCKET_NAME}/llm-finetune-dataset-small/train.jsonl\"\nVALIDATION_DATASET = f\"gs://{GCS_BUCKET_NAME}/llm-finetune-dataset-small/test.jsonl\"' cli.py && sed -n 8,13p cli.py"
step 'python -c "import cli; print(cli.TRAIN_DATASET); print(cli.VALIDATION_DATASET)"'
step 'GCS_BUCKET_NAME=my-own-bucket python -c "import cli; print(cli.TRAIN_DATASET)"'
step 'env -u GCS_BUCKET_NAME python cli.py --help 2>&1 | tail -4'
cd /repo/dataset-creator
step 'env -u GCP_PROJECT python cli.py --help 2>&1 | tail -4'
