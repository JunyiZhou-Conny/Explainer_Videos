# @title Run Demo

async def run_demo() -> list[dict]:
  DEMO_MONTH = date.today().strftime("%Y-%m")
  DEMO_BRAND = "Formaggio.me"
  OUTPUT_DIR = Path("/content/newsletter_output")

  # Orchestrator
  print("\n[agent] Building orchestrator...")
  orchestrator_agent = build_orchestrator()

  batch_id = uuid4().hex[:8]
  receipts = []
  async with orchestrator_agent:
      for index, user in enumerate(USERS, start=1):
          settings = Settings(
              city=user["city"],
              month=DEMO_MONTH,
              brand=DEMO_BRAND,
              recipient=user["email"],
              name=user["name"],
              output=OUTPUT_DIR / f"{user['name']}-{DEMO_MONTH}-{batch_id}.html",
          )

          receipt = await generate_newsletter(settings, orchestrator_agent, invoke_agent)
          assert receipt["status"] == "saved" and receipt["email_sent"] is False
          receipts.append(receipt)

  assert len(receipts) == len(USERS)
  print(f"\nCreated {len(receipts)} mock emails. No email was sent.")
  return receipts

receipts = await run_demo()
receipts
