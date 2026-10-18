# @title Business Logic

#########################
# Business Logic
#########################
def validate_newsletter(draft: Newsletter, evidence: Evidence, settings: Settings) -> None:
    """Verify structure, source membership, and stated expiration dates.

    A source ID proves the URL was returned by search; it does not prove a claim
    is true. The researcher/editor still have to check support and relevance.
    """
    if not evidence.sources:
        raise ValueError("No search-grounded sources were returned; refusing an unsourced newsletter.")
    titles = set()
    for item in [*draft.news, *draft.offers]:
        title = item.title.casefold()
        if title in titles:
            raise ValueError("Remove duplicate story/offer titles.")
        titles.add(title)
        if len(item.source_ids) != len(set(item.source_ids)):
            raise ValueError("A story cannot repeat a source ID.")
        for source_id in item.source_ids:
            if source_id not in evidence.sources or not safe_url(evidence.sources[source_id]["url"]):
                raise ValueError(f"Unknown or unsafe source {source_id!r}; use the supplied source registry.")
    period_start = date.fromisoformat(settings.month + "-01")
    # Historical issues may discuss offers from that month, explicitly archived.
    cutoff = max(period_start, date.today()) if settings.month >= date.today().strftime("%Y-%m") else period_start
    for offer in draft.offers:
        if offer.valid_until != "unknown":
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", offer.valid_until):
                raise ValueError("Offer expiration must be YYYY-MM-DD or 'unknown'.")
            if date.fromisoformat(offer.valid_until) < cutoff:
                raise ValueError(f"Offer {offer.title!r} expires before the issue's relevant date.")

def render_email(draft: Newsletter, evidence: Evidence, settings: Settings) -> str:
    """Render the validated newsletter to a self-contained HTML preview.

    Every model-supplied string is HTML-escaped, so hostile text in a summary
    cannot inject markup or script into the saved page.
    """
    def paragraph(text: str) -> str:
        return escape(text).replace("\n", "<br>")

    def card(item: Story) -> str:
        links = " · ".join(
            f'<a href="{escape(evidence.sources[key]["url"], quote=True)}" target="_blank" '
            f'rel="noopener noreferrer">{escape(evidence.sources[key]["title"])}</a>'
            for key in item.source_ids)
        expiry = ""
        if isinstance(item, Offer):
            label = (f"Published expiry: {item.valid_until}" if item.valid_until != "unknown"
                     else "Expiry not published — check with the retailer")
            expiry = f'<p class="detail">{escape(label)}</p>'
        return (f'<article><h3>{escape(item.title)}</h3><p>{paragraph(item.summary)}</p>'
                f'{expiry}<p class="sources">Source: {links}</p></article>')

    news = "".join(card(item) for item in draft.news)
    offers = "".join(card(item) for item in draft.offers)
    archive = ('<p class="archive">Archive edition: offers may no longer be available.</p>'
               if settings.month < date.today().strftime("%Y-%m") else "")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(draft.subject)}</title>
<style>
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #f3efe5; color: #263e32; font: 16px/1.65 Georgia, serif; }}
.envelope {{ max-width: 760px; margin: 24px auto 12px; padding: 0 24px; font: 13px/1.7 Arial, sans-serif; color: #59665b; overflow-wrap: anywhere; }}
.sheet {{ max-width: 712px; margin: 0 auto 40px; background: #fffdf7; border: 1px solid #dcd9c9; }}
header {{ padding: 34px 40px; background: #234b38; color: #fff8de; }}
.eyebrow {{ font: 12px/1.5 Arial, sans-serif; letter-spacing: 2px; text-transform: uppercase; }}
header h1 {{ margin: 12px 0 4px; font-size: 38px; font-weight: normal; line-height: 1.2; }}
header p {{ margin: 12px 0 0; color: #dfe5ce; }}
main {{ padding: 28px 40px; }}
h2 {{ margin: 30px 0 12px; font: bold 12px/1.5 Arial, sans-serif; letter-spacing: 2px; text-transform: uppercase; color: #76551d; }}
h3 {{ margin: 0 0 8px; font-size: 23px; font-weight: normal; line-height: 1.35; }}
article {{ border-top: 1px solid #dedcca; padding: 20px 0; }}
p {{ margin: 8px 0 16px; }}
a {{ color: #245e43; text-decoration-thickness: 1px; text-underline-offset: 3px; overflow-wrap: anywhere; }}
.sources, .detail, footer, .archive {{ font: 12px/1.6 Arial, sans-serif; color: #64705f; }}
.offers {{ padding: 2px 20px 12px; background: #f5eed8; }}
.archive {{ background: #f5eed8; padding: 10px; color: #684a18; }}
footer {{ padding: 24px 40px; border-top: 1px solid #dedcca; }}
@media (max-width: 560px) {{ header, main, footer {{ padding: 24px; }} header h1 {{ font-size: 30px; }} .sheet {{ margin: 0 12px 24px; }} }}
</style></head><body>
<div class="envelope"><strong>LOCAL EMAIL PREVIEW · NOT SENT</strong><br>
From: {escape(settings.brand)}<br>To: {escape(settings.name)} &lt;{escape(settings.recipient)}&gt;<br>Subject: {escape(draft.subject)}</div>
<div class="sheet"><header><div class="eyebrow">{escape(settings.brand)} · The cheese letter</div>
<h1>{escape(settings.city)}, with cheese.</h1><p>{escape(settings.month)} edition</p></header>
<main>{archive}<p>Hi {escape(settings.name)},</p><p>{paragraph(draft.introduction)}</p>
<h2>From the cheese counter</h2>{news}
<div class="offers"><h2>Offers &amp; discoveries</h2><p>{paragraph(draft.offers_note)}</p>{offers}</div>
<p style="margin-top: 28px">{paragraph(draft.closing)}</p></main>
<footer>Created {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC} · AC215 Fall 2026<br>
This is a locally saved email preview. No email was sent. Prices and availability can change.
</footer></div></body></html>"""

def save_email(draft: Newsletter, evidence: Evidence, settings: Settings) -> dict:
    """Validate, render, and write the HTML preview locally. Returns a receipt."""
    validate_newsletter(draft, evidence, settings)
    document = render_email(draft, evidence, settings)
    target = settings.output.resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(document, encoding="utf-8")
    return {"status": "saved", "email_sent": False,
            "path": str(target), "bytes": len(document.encode("utf-8"))}

async def generate_newsletter(
    settings: Settings, agent: object,
    invoke_agent: Callable[..., Awaitable[str]],
) -> dict:
    """Let the orchestrator choose its tools; verify success from Python state."""
    context = NewsletterContext(settings)
    request = {"city": settings.city, "issue_month": settings.month,
               "brand": settings.brand, "today": date.today().isoformat()}

    print(f"Generating newsletter for {settings.city} · {settings.month}", flush=True)
    reply = await invoke_agent(agent, json.dumps(request), context)
    if context.receipt is None:
        raise RuntimeError(f"No successful tool receipt. Orchestrator response: {reply}")

    receipt = context.receipt
    if not Path(receipt["path"]).is_file():
        raise RuntimeError("The mock email receipt points to a file that does not exist.")
    print(f"Saved HTML: {receipt['path']} ({receipt['bytes']} bytes). No email sent.")
    return receipt
