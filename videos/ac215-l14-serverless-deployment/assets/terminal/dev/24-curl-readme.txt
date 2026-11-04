$ FUNCTION_URL=http://localhost:8080
curl --get "$FUNCTION_URL" \
  --data-urlencode 'text=Good afternoon everyone' \
  --data-urlencode 'src=en' --data-urlencode 'dest=fr'
Bonjour à tous
[exit 0]
