# B3: flag order. main() runs generate, prepare, upload in that order, whatever order you type the flags.
cd /repo/dataset-creator
mkdir -p data && cp /repo/scripted/cheese_qa_*.txt data/
step 'python cli.py --upload --prepare > /tmp/out.txt 2>&1; echo "cli.py exit status: $?"; grep -v "^  " /tmp/out.txt'
step 'ls data'
