# m6_chroma.py: what 6-rag/2-custom-chromadb-rag's healthcheck and README ask of today's Chroma server
# (the image L05/L06's captures pulled as chromadb/chroma:latest), from a container on the same network.
import urllib.request, urllib.error
for path in ["/api/v1/heartbeat", "/api/v2/heartbeat"]:
    try:
        with urllib.request.urlopen("http://llm-rag-chromadb:8000" + path) as r:
            print(path, "->", r.status, r.read().decode())
    except urllib.error.HTTPError as e:
        print(path, "->", e.code, e.read().decode())
