df = pd.read_json('train_16k.jsonl', lines=True)
df = df.sample(n=1000,random_state=42).reset_index(drop=True) #Sampling 1000 data points due to computation time constraints
print(df.shape)
print(df.iloc[0]['contents'])
df.head(2)