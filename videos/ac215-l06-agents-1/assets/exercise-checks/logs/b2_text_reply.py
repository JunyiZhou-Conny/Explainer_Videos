# b2_text_reply.py: cli.agent() of the B2 copy (no tool_config), with a stand-in model reply that is plain text
# (no function call): which lines of cli.py run, and how many model calls are made?
from standin import install, reply, Part
import cli
seen = install([reply(Part(text="(stand-in reply: plain text, no function call)"))])
cli.agent(method="char-split")
print("model calls made:", len(seen))
