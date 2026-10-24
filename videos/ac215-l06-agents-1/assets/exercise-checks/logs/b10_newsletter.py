# b10_newsletter.py: the Newsletter's own Python (cells 9, 16 [the redacted copy], 18, 20: imports, contracts,
# validation, rendering, the receipt check, the send_email tool), with no model. invoke_agent is replaced by
# stand-ins that do what an orchestrator could do, calling the notebook's own functions.
import asyncio, os, re
from datetime import date
from pathlib import Path
from notebook import run_cells
nb = run_cells("cheese-newsletter", ["09", "16.redacted", "18", "20"])
Settings, Newsletter, Story, Offer = nb["Settings"], nb["Newsletter"], nb["Story"], nb["Offer"]
review_draft, send_newsletter, generate_newsletter = nb["review_draft"], nb["send_newsletter"], nb["generate_newsletter"]
month = date.today().strftime("%Y-%m")
def settings(name):
    return Settings(city="Summerville", month=month, brand="Formaggio.me", recipient="reader@example.com",
                    name=name, output=Path(f"/tmp/newsletter_output/{name}-{month}-check.html"))
def draft(offer_summary):
    return Newsletter(subject="Cheese in Summerville", introduction="Hello from the cheese counter.",
        news=[Story(title="A cheese fair", summary="A local fair features farmhouse cheeses.", source_ids=["S1"])],
        offers=[Offer(title="Brie of the week", summary=offer_summary, source_ids=["S2"], valid_until="unknown")],
        offers_note="Offers as published by the retailer.", closing="See you next month.")
def research(ctx):
    ctx.evidence.add("https://example.com/cheese-fair", "Cheese fair")
    ctx.evidence.add("https://shop.example.com/brie", "Brie offer")
    ctx.research.append("(stand-in research brief)")
URL_SUMMARY = "Brie is 20% off this week. Promotion URL: https://shop.example.com/brie?promo=1"

async def says_done(agent, prompt, context):
    return "Newsletter sent successfully!"
async def sends_url_draft(agent, prompt, context):
    research(context)
    print("  editor's draft reviewed:", {k: v for k, v in review_draft(context, draft(URL_SUMMARY)).items() if k != "draft"})
    print("  send_email ->", send_newsletter(context))
    return "done!"
async def sends_then_file_vanishes(agent, prompt, context):
    await sends_url_draft(agent, prompt, context)
    os.remove(context.receipt["path"])
    return "done!"

async def main():
    for name, standin in [("says-done", says_done), ("sends", sends_url_draft), ("file-gone", sends_then_file_vanishes)]:
        print(f"== stand-in orchestrator: {name}")
        try:
            await generate_newsletter(settings(name), None, standin)
        except RuntimeError as e:
            print("  RuntimeError:", e)
asyncio.run(main())

print("\n== the editor's rule as a check: five lines added at the end of validate_newsletter (cell 18)")
src = Path("/cells/cheese-newsletter/cell-18.py").read_text().split("\n")
assert src[32].strip().startswith('raise ValueError(f"Offer {offer.title!r} expires')
added = ['    URL = re.compile(r"https?://|www\\.", re.IGNORECASE)',
         '    for text in [draft.subject, draft.introduction, draft.offers_note, draft.closing,',
         '                 *(f"{item.title} {item.summary}" for item in [*draft.news, *draft.offers])]:',
         '        if URL.search(text):',
         '            raise ValueError("Remove embedded URLs from the newsletter text; sources are linked by ID.")']
print("\n".join(added))
exec(compile("\n".join(src[:33] + added + src[33:]), "cell-18 (patched)", "exec"), nb)
ctx = nb["NewsletterContext"](settings("patched")); research(ctx)
print("review_draft ->", {k: v for k, v in nb["review_draft"](ctx, draft(URL_SUMMARY)).items() if k != "draft"})
print("send_email   ->", nb["send_newsletter"](ctx), "| receipt:", ctx.receipt)
ok = draft("Brie is 20% off this week at the retailer's Summerville store.")
print("without the URL: review_draft ->", nb["review_draft"](ctx, ok)["status"])

print("\n== Settings checks the USERS entries before any API call")
for email in ["reader@example.com", "<email>", "sam at example.com"]:
    try:
        Settings(city="Charlotte", month=month, brand="Formaggio.me", recipient=email, name="Sam",
                 output=Path("/tmp/x.html")); print(f"  recipient {email!r}: ok")
    except ValueError as e:
        print(f"  recipient {email!r}: ValueError: {e}")
