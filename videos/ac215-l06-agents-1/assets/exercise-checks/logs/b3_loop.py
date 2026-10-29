# b3_loop.py <scenario>: cli.agent() of the B3 copy (the capped loop), with stand-in model replies.
#   three-steps : call get_book_by_author, then call get_book_by_search_content, then plain text
#   never-stops : every reply is a function call
#   real-third  : two scripted calls, then the real SDK builds request 3 (built, not sent)
import sys
from standin import install, reply, call, Part, stored_vector
import cli
scenario = sys.argv[1]
cli.generate_query_embedding = stored_vector("Hand-book on cheese making", "rennet")
c1 = call("get_book_by_author", author="George E. Newell", search_content="How much rennet should be added to the milk?")
c2 = call("get_book_by_search_content", search_content="Which books mention goat cheese?")
if scenario == "three-steps":
    seen = install([reply(c1), reply(c2), reply(Part(text="(stand-in reply: plain text, no function call)"))])
elif scenario == "never-stops":
    seen = install([reply(c1)])
else:
    seen = install([reply(c1), reply(c2)], real_last=True)
cli.agent(method="char-split")
print("model calls made:", len(seen))
