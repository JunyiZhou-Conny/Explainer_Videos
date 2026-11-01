printf '```json\n[{"question": "What is the rind of Camembert made of?", "answer": "Good question! A bloomy white mould. (scripted)"},\n {"question": "Why is Halloumi good for grilling?", "answer": "Glad you ask! Its high melting point. (scripted)"}]\n```\n' > data/cheese_qa_5.txt
printf '[{"question": "What is a washed-rind cheese?", "answer": "I have slides for that! Brine. (scripted)"},\n {"question": "How long is Comte aged?", "answer": "Remember rule number 672, at least four months, and the best' > data/cheese_qa_6.txt
python cli.py --prepare
