# b3.patch.py <cli.py>: exercise B3. Replaces the two hand-written calls (cli.py:439-478) with a loop of at
# most 5 steps that runs every function call the model asks for and stops when a reply has none.
import sys
p = sys.argv[1]
lines = open(p).read().split("\n")
assert lines[438].strip().startswith("# Step 1: Prompt LLM"), lines[438]
assert lines[477].strip() == 'print("\\n\\n\\n\\nLLM Response:", response)', lines[477]
assert lines[480].startswith("def main("), lines[480]
loop = '''    contents = [user_prompt_content]
    config = types.GenerateContentConfig(temperature=0, tools=[agent_tools.cheese_expert_tool])
    for step in range(5):
        response = llm_client.models.generate_content(
            model=GENERATIVE_MODEL, contents=contents, config=config)
        model_turn = response.candidates[0].content
        calls = [p.function_call for p in model_turn.parts if p.function_call]
        if not calls:                      # final answer: no more tool requests
            print("Answer:", response.text)
            break
        contents.append(model_turn)        # keep the model's turn verbatim (thought signatures)
        contents.append(Content(role="user", parts=agent_tools.execute_function_calls(
            calls, collection, embed_func=generate_query_embedding)))
    else:
        print("Gave up after 5 steps")'''.split("\n")
lines[438:478] = loop
open(p, "w").write("\n".join(lines))
