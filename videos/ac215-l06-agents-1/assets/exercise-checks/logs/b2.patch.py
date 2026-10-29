# b2.patch.py <cli.py>: exercise B2. Deletes the tool_config block of call 1 (cli.py:447-451) and asks
# "Hi! Who are you?" instead of the cheese question (cli.py:435).
import sys
p = sys.argv[1]
lines = open(p).read().split("\n")
assert lines[434].strip().startswith('Part(text="Describe where cheese making'), lines[434]
assert lines[446].strip() == "tool_config=types.ToolConfig(" and lines[450].strip() == ")", lines[446:451]
lines[434] = '            Part(text="Hi! Who are you?"),'
del lines[446:451]
open(p, "w").write("\n".join(lines))
