# B1: two broken batches beside the five scripted ones, made with exercises.md's commands exactly as printed
# (snippets/b1-batches.sh): a batch wrapped in a ```json fence, and a batch cut off mid-answer.
cd /repo/dataset-creator
mkdir -p data && cp /repo/scripted/cheese_qa_*.txt data/
step 'cat /checks/snippets/b1-batches.sh'
step 'sh /checks/snippets/b1-batches.sh'
step 'wc -l data/train.jsonl data/test.jsonl'
