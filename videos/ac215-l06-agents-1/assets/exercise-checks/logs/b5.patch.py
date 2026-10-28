# b5.patch.py <conditional_agent.py>: writes the two fixes of exercise B5 next to the file, leaving it unchanged:
#   conditional_agent_lower.py  : line 85 normalizes the label with .strip().lower()
#   conditional_agent_schema.py : the classifier gets output_schema=Classification (a Literal of the three labels),
#                                 and line 85 reads the field from the dict that output_key now stores
import sys, pathlib
p = pathlib.Path(sys.argv[1])
src = p.read_text()
line85 = '        complexity = ctx.session.state.get("query_complexity", "simple")\n'
assert src.count(line85) == 1
lower = src.replace(line85, '        complexity = ctx.session.state.get("query_complexity", "simple").strip().lower()\n')
(p.parent / "conditional_agent_lower.py").write_text(lower)
schema = src.replace(line85, '        complexity = ctx.session.state.get("query_complexity", {}).get("complexity", "simple")\n')
imp = "from google.genai import types\n"
assert schema.count(imp) == 1
schema = schema.replace(imp, imp + "from typing import Literal\nfrom pydantic import BaseModel\n\n\n"
                        "class Classification(BaseModel):\n"
                        "    complexity: Literal[\"simple\", \"complex\", \"ambiguous\"]\n")
key = '        output_key="query_complexity"\n    )'
assert schema.count(key) == 1
schema = schema.replace(key, '        output_key="query_complexity",\n        output_schema=Classification,\n    )')
(p.parent / "conditional_agent_schema.py").write_text(schema)
