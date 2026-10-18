steps = reasoning_result["reasoning_steps"]

display(Markdown("## Analysis\n" + steps["analysis"]))

for i, qa in enumerate(steps["qa_pairs"], 1):
    display(Markdown(
        f"## Sub-question {i}: {qa['question']}\n\n"
        f"### Answer\n{qa['answer']}\n\n"
        f"### Verification\n{qa['verification']}"
    ))

display(Markdown(
    "## Final synthesis\n" + reasoning_result["response"]
))
