# Helper checks (B7, C8), run inside python:3.12-slim-bookworm with --network none: tutorial/ at 46cc62f
# mounted read-only at /repo/tutorial. No gcloud is installed in this container (C8 depends on that).
. /checks/lib.sh
mkdir -p /tmp/w && cd /tmp/w && cp /repo/tutorial/app/examples/passage.txt ./passage.txt
H='python /repo/tutorial/run_job.py ./passage.txt --project=your-project-id --region=northamerica-northeast2 --job=translation-audio --input-bucket=YOUR_INPUT_BUCKET --output-bucket=YOUR_OUTPUT_BUCKET'
step "$H --src=en --dest=fr --download-dir=./results --dry-run"
step "$H --src=en --download-dir=./results --dry-run | grep -o -- '--args=[^ ]*'"
step "$H --src=en --dest=es --no-download --dry-run"
step "python /repo/tutorial/run_job.py ./passage.txt --project=your-project-id --input-bucket=gs://YOUR_INPUT_BUCKET --output-bucket=YOUR_OUTPUT_BUCKET --dry-run 2>&1 | tail -1"
step "python /repo/tutorial/run_job.py ./passage.txt --project=your-project-id --input-bucket=YOUR_INPUT_BUCKET --output-bucket=YOUR_OUTPUT_BUCKET --dest=es,de --dry-run 2>&1 | tail -1"
step "python -c 'print(\"a\" * 5001)' > long.txt; python /repo/tutorial/run_job.py ./long.txt --project=your-project-id --input-bucket=YOUR_INPUT_BUCKET --output-bucket=YOUR_OUTPUT_BUCKET --dry-run 2>&1 | tail -1"
step "command -v gcloud || echo 'no gcloud on PATH'; $H --src=en --dest=fr --download-dir=./results; echo \"exit status: \$?\""
step "ls -A /tmp/w"
