$ curl -sS -w '\n[HTTP %{http_code}]\n' --max-time 5 http://localhost:900/api/docs
curl: (7) Failed to connect to localhost:900 after 0 ms: Could not connect to server

[HTTP 000]
[exit 7]
