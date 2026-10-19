# c3_second_call.py: cli.agent() of the copy with print(response.text), when call 2 answers with ANOTHER
# function call (possible: call 2 has tools but no tool_config, so the mode is AUTO). Reply 1 is the staff's
# recorded call (out.txt:20-28, with its thought signature); reply 2 is a stand-in function call.
import ast
from standin import install, reply, call, Part, stored_vector, types
import cli
cli.generate_query_embedding = stored_vector("Tolminc Cheese", "curd")
rec = open("/app/out.txt").read().splitlines()
sig = ast.literal_eval(rec[27].strip().removeprefix("thought_signature=").rstrip(","))
first = Part(function_call=types.FunctionCall(id="call_1212960", name="get_book_by_author",
             args={"author": "Pavlos Protopapas", "search_content": "cheese making importance location"}),
             thought_signature=sig)
seen = install([reply(first), reply(call("get_book_by_search_content", search_content="cheese caves of the valley"))])
cli.agent(method="char-split")
print("model calls made:", len(seen))
