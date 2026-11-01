# B4: which rows survive drop_duplicates (line 233) and dropna (line 234); exercises.md's block exactly as printed.
cd /repo/dataset-creator
mkdir -p data && cp /repo/scripted/cheese_qa_*.txt data/
step 'sh /checks/snippets/b4-batch.sh | sed -n 1,2p\;8,12p'
step 'grep -c "" data/instruct-dataset.csv; grep -i "rennet do" data/instruct-dataset.csv | cut -c1-90; grep -c "Is Feta\|Is Mozzarella" data/instruct-dataset.csv'
