## Histogram for number of tokens in the dataset
temp = train_dataset.to_pandas()
plt.figure(figsize=(8, 4))
temp['text'].apply(lambda x: len(tokenizer.encode(x))).hist(bins=50)
plt.xlabel('Number of Tokens')
plt.ylabel('Frequency')
plt.title('Distribution of Token Counts in Training Dataset')
plt.grid(axis='y', alpha=0.75)
plt.show()