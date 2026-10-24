# request_call1.py: runs cli.agent() unchanged, with the SDK's transport replaced by a function that prints the
# request it would send and stops (as the video's cli-container/31 capture does): built, not sent.
import json, sys
sys.path.insert(0, "/app")
import cli
api = cli.llm_client._api_client
def show(method, path, body, http_options=None):     # stands in for the HTTPS request
    req = api._build_request(method, path, body, http_options)
    print(method.upper(), req.url)
    print(json.dumps(body, indent=2)[:4000])
    print("top-level keys:", list(body))
    raise SystemExit("-- stopped here: nothing was sent to Vertex AI --")
api.request = show
cli.agent(method="char-split")
