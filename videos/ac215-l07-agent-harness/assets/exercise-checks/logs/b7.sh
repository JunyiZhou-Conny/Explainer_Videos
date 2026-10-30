# B7: the injection detector on the four vendor documents (Act 4, scripted planner, test decline).
for doc in clean benign quoted malicious; do
  step "python cli.py --act 4 --fixture --vendor-document $doc --email-decision decline | grep -E 'Vendor evidence|HARNESS|Model calls'"
done
step "python -c 'from formaggio.shop.vendor_outreach import detect_injection; from formaggio.config import load_json; [print(k, detect_injection(v)) for k, v in load_json(\"vendor_documents.json\").items()]'"
