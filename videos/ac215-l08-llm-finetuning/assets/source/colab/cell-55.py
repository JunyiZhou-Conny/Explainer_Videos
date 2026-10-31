def extract_qa(row):
    question = ""
    answer = ""
    for item in row['contents']:
        if item['role'] == 'user':
            question = item['parts'][0]['text']
        elif item['role'] == 'model':
            answer = item['parts'][0]['text']
    return pd.Series({'question': question, 'answer': answer})

df[['question', 'answer']] = df.apply(extract_qa, axis=1)
df = df[['question', 'answer']].reset_index(drop=True)
display(df.head())

df.iloc[0].values