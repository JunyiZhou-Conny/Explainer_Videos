# b7.patch.py: exercise B7's fix in a copy of the module, litellm_agent/ (2-litellm/ stays as committed):
# root_agent uses LiteLlm with a provider-prefixed model name. Also makes a second copy named litellm/.
import pathlib, shutil
root = pathlib.Path(".")
for name in ("litellm_agent", "litellm"):
    shutil.copytree(root / "2-litellm", root / name)
p = root / "litellm_agent" / "agent.py"
src = p.read_text()
old = 'root_agent = LlmAgent(\n    model="gpt-4",'
assert src.count(old) == 1
src = src.replace("from google.adk.agents import LlmAgent\n",
                  "from google.adk.agents import LlmAgent\nfrom google.adk.models.lite_llm import LiteLlm\n")
src = src.replace(old, 'root_agent = LlmAgent(\n    model=LiteLlm(model="openai/gpt-5.6-luna"),')
p.write_text(src)
