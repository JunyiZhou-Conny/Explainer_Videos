# standin.py: stand-ins for the two things in llm-rag's agent() that need Google, so the rest of the code
# (cli.py, agent_tools.py, Chroma) runs unchanged without a key:
#   - the query embedding: a function that returns the stored vector of one chunk of the collection
#     (so WHICH chunks come back is not what a real query would return; the filters and the code path are real);
#   - the model's replies: scripted GenerateContentResponse objects, written here by hand and printed as
#     "[stand-in model]". They are not model output; they only drive cli.py down a given path.
# Used by the b1/b2/b3/c3 checks. Run inside the llm-rag venv with /app = an llm-rag work copy.
import sys
sys.path.insert(0, "/app")
import cli, agent_tools                                     # noqa: E402
from google.genai import types                              # noqa: E402
from google.genai.types import Content, Part                # noqa: E402


def collection():
    return cli.chromadb.HttpClient(host=cli.CHROMADB_HOST, port=cli.CHROMADB_PORT).get_collection(
        "char-split-collection")


def stored_vector(book, word):
    t = collection().get(where={"book": book}, include=["embeddings", "documents"])
    i = next(k for k, d in enumerate(t["documents"]) if word in d)
    print(f"[stand-in] embed_func returns the stored vector of chunk {t['ids'][i]} "
          f"({book!r}, its first chunk containing {word!r})")
    v = [float(x) for x in t["embeddings"][i]]
    return lambda text: v


def call(name, **args):
    return Part(function_call=types.FunctionCall(name=name, args=args))


def reply(*parts):
    return types.GenerateContentResponse(candidates=[types.Candidate(
        content=Content(role="model", parts=list(parts)), finish_reason="STOP")])


def install(replies, real_last=False):
    """Replace llm_client.models.generate_content; reply k answers model call k (the last one repeats).
    With real_last, the call after the scripted replies goes to the real SDK, whose transport is replaced
    by a function that prints a summary of the request body and stops (built, not sent)."""
    seen = []
    real = cli.llm_client.models.generate_content

    def generate_content(*, model, contents, config=None):
        n = len(seen) + 1
        cs = contents if isinstance(contents, list) else [contents]
        tc = getattr(config, "tool_config", None)
        mode = tc.function_calling_config.mode if tc and tc.function_calling_config else None
        kinds = [[("function_call" if p.function_call else "function_response" if p.function_response
                   else "text") for p in c.parts] for c in cs]
        print(f"[stand-in model] call {n}: contents roles {[c.role for c in cs]}, parts {kinds}, "
              f"tools {'yes' if config is not None and config.tools else 'no'}, tool_config mode {mode}")
        seen.append(cs)
        if real_last and n > len(replies):
            api = cli.llm_client._api_client

            def show(method, path, body, http_options=None):
                print("[built, not sent] request body: contents roles",
                      [c.get("role") for c in body["contents"]], "| parts",
                      [[next(iter(p)) for p in c["parts"]] for c in body["contents"]],
                      "| toolConfig" , body.get("toolConfig"))
                raise SystemExit("-- stopped here: nothing was sent to Vertex AI --")
            api.request = show
            return real(model=model, contents=contents, config=config)
        return replies[min(n, len(replies)) - 1]

    cli.llm_client.models.generate_content = generate_content
    return seen
