# c3.patch.py <cli.py>: the video's fix for the README slip (S07): line 478 prints response.text instead of
# the whole response object.
import sys
p = sys.argv[1]
lines = open(p).read().split("\n")
assert lines[477].strip() == 'print("\\n\\n\\n\\nLLM Response:", response)', lines[477]
lines[477] = '        print(response.text)'
open(p, "w").write("\n".join(lines))
