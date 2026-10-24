$ curl -s -w 'HTTP %{http_code}\n' https://storage.googleapis.com/storage/v1/b/cheese-app-trainer
{
  "error": {
    "code": 401,
    "message": "Anonymous caller does not have storage.buckets.get access to the Google Cloud Storage bucket. Permission 'storage.buckets.get' denied on resource '//storage.googleapis.com/projects/_/buckets/cheese-app-trainer' (or it may not exist).",
    "errors": [
      {
        "message": "Anonymous caller does not have storage.buckets.get access to the Google Cloud Storage bucket. Permission 'storage.buckets.get' denied on resource '//storage.googleapis.com/projects/_/buckets/cheese-app-trainer' (or it may not exist).",
        "domain": "global",
        "reason": "required",
        "locationType": "header",
        "location": "Authorization"
      }
    ]
  }
}
HTTP 401
[exit 0]
