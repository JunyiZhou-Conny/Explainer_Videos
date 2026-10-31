# Split the dataset into train and test
dataset = dataset.train_test_split(test_size=0.10, shuffle=True, seed = 42)

# Now you have a DatasetDict with 'train' and 'test' splits
train_dataset = dataset['train']
test_dataset = dataset['test']

print(train_dataset.shape)
print(test_dataset.shape)