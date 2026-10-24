# @title The Customer Request

request = load_scenario("standard")
display(customer_ask(request))
print()
print("Structured fields the application actually trusts:")
print(json.dumps(request.model_dump(mode="json"), indent=2))
