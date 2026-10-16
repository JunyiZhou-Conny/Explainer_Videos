# check-only (B6): what chat()'s generate_content call would send to Vertex AI, with and without the fix.
# The request is captured just before it leaves (BaseApiClient.request is replaced), so no key is needed and
# nothing reaches Google. The SYSTEM_INSTRUCTION text is read from the tutorial's cli.py with ast (no import).
import ast, json
from google import genai
from google.genai import types

tree = ast.parse(open("/app/cli.py").read())
SYSTEM_INSTRUCTION = next(n.value.value for n in tree.body if isinstance(n, ast.Assign)
                          and getattr(n.targets[0], "id", "") == "SYSTEM_INSTRUCTION")
llm_client = genai.Client(vertexai=True, project="your-project-id", location="global")

class Stop(Exception):
    pass
def capture(http_method, path, request_dict, http_options=None):
    print("  POST", path)
    print("  request keys:", sorted(request_dict))
    if "systemInstruction" in request_dict:
        si = request_dict["systemInstruction"]
        print("  systemInstruction:", json.dumps(si)[:110], "...")
    raise Stop
llm_client._api_client.request = capture

INPUT_PROMPT = "\n\tWhat is the capital of France?\n\t(ten retrieved chunks would follow here)\n\t"
for label, kw in [("as in cli.py:394-396", {}),
                  ("with the fix", {"config": types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION)})]:
    print(label + ":")
    try:
        llm_client.models.generate_content(model="gemini-3.1-flash-lite", contents=INPUT_PROMPT, **kw)
    except Stop:
        pass
