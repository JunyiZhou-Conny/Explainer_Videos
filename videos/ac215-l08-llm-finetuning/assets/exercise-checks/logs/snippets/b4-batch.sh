cat > data/cheese_qa_7.txt <<'EOF'
[
  {"question": "What does rennet do in cheesemaking?", "answer": "Good question! A second answer. (scripted)"},
  {"question": "what does rennet do in cheesemaking?", "answer": "Good question! Lower case. (scripted)"},
  {"question": "Is Feta a brined cheese?"},
  {"question": "Is Mozzarella stretched?", "answer": null}
]
EOF
python cli.py --prepare
