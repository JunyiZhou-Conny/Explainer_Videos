# @title Catalog Data & Utils

#########################
# Data
#########################
# Edit this list to add readers or change their details. Email is preview-only.
USERS = [
    {"name": "<reader1>", "email": "<email>", "city": "Summerville"},
    {"name": "<reader2>", "email": "<email>", "city": "Charlotte"},
    # {"name": "<reader3>", "email": "<email>", "city": "Atlanta"},
    # {"name": "<reader4>", "email": "<email>", "city": "Cambridge"},
]

#########################
# Data Contracts
#########################
class Story(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    title: str = Field(min_length=1, max_length=160)
    summary: str = Field(min_length=1, max_length=1200)
    source_ids: list[str] = Field(min_length=1, max_length=5)

class Offer(Story):
    valid_until: str = Field(description="Published expiration date YYYY-MM-DD, or 'unknown'.")

class Newsletter(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    subject: str = Field(min_length=1, max_length=160)
    introduction: str = Field(min_length=1, max_length=900)
    news: list[Story] = Field(min_length=1, max_length=5)
    offers: list[Offer] = Field(max_length=4)
    offers_note: str = Field(min_length=1, max_length=600)
    closing: str = Field(min_length=1, max_length=500)

@dataclass
class Evidence:
    """Framework-neutral source registry with stable S1/S2/... identifiers.

    Adapters must add only sources returned by search citation metadata.
    Registry membership does not establish that a source supports a claim.
    """
    sources: dict[str, dict[str, str]] = field(default_factory=dict)

    def add(self, url: str, title: str = "") -> None:
        """Register a safe source once, preserving its first title and ID."""
        if not safe_url(url) or any(source["url"] == url for source in self.sources.values()):
            return
        self.sources[f"S{len(self.sources) + 1}"] = {
            "title": title or "Research source", "url": url,
        }

@dataclass(frozen=True)
class Settings:
    """Everything the application controls for one newsletter run.

    The model never sets these; the CLI does. __post_init__ validates them up
    front so a bad city/month/recipient/output fails before any API call.
    """
    city: str
    month: str
    brand: str
    recipient: str
    output: Path
    name: str = "Reader"

    def __post_init__(self):
        for label, text in (("city", self.city), ("brand", self.brand), ("name", self.name)):
            if not text.strip() or len(text) > 120 or any(ord(c) < 32 for c in text):
                raise ValueError(f"{label} must be 1-120 characters without control characters.")
        if not re.fullmatch(r"\d{4}-\d{2}", self.month):
            raise ValueError("Use month YYYY-MM, for example 2026-09.")
        date.fromisoformat(self.month + "-01")
        if not re.fullmatch(r"[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+", self.recipient):
            raise ValueError("Use a single email-shaped preview recipient, such as reader@example.com.")
        if self.output.suffix.lower() != ".html":
            raise ValueError("The output filename must end with .html.")

@dataclass
class NewsletterContext:
    """Application-owned state for one reader's newsletter generation."""
    settings: Settings
    evidence: Evidence = field(default_factory=Evidence)
    research: list[str] = field(default_factory=list)
    draft: Newsletter | None = None
    receipt: dict | None = None

#########################
# Utils
#########################
def safe_url(value: str) -> bool:
    """Only allow ordinary HTTP(S) links in the generated document."""
    try:
        url = urlsplit(value)
        return (url.scheme in ("http", "https") and bool(url.hostname)
                and url.username is None and url.password is None
                and not any(c.isspace() or ord(c) < 32 for c in value))
    except ValueError:
        return False

def specialist_request(context: NewsletterContext, task: str) -> str:
    """Supply specialists with application-owned requirements and current work."""
    settings = context.settings
    return json.dumps({
        "task": task, "city": settings.city, "issue_month": settings.month,
        "brand": settings.brand, "today": date.today().isoformat(),
        "research_briefs": context.research, "source_registry": context.evidence.sources,
        "draft": context.draft.model_dump() if context.draft else None,
    })

def review_draft(context: NewsletterContext, draft: Newsletter) -> dict:
    """Store the editor's work and report deterministic validation errors."""
    context.draft = draft
    try:
        validate_newsletter(draft, context.evidence, context.settings)
    except ValueError as exc:
        return {"status": "error", "message": str(exc), "draft": draft.model_dump()}
    return {"status": "ready", "draft": draft.model_dump()}

def send_newsletter(context: NewsletterContext) -> dict:
    """Mock-send the editor's current draft by saving a local HTML preview.

    Requires a draft and search-backed evidence. On validation failure, ask the
    specialists to revise and retry. A saved receipt means stop. No email is sent.
    Recipient and output path are fixed by the application, not tool arguments.
    """
    if context.receipt is not None:
        return context.receipt
    if context.draft is None:
        return {"status": "error", "message": "No draft. Call editor_agent first."}
    return save_newsletter(context, context.draft.model_dump_json())

def save_newsletter(context: NewsletterContext, newsletter_json: str) -> dict:
    """Validate newsletter JSON and save a local HTML email preview.

    Use the Newsletter schema and only supplied source IDs. The application
    fixes sender, recipient, and output path. No email is sent. On an error,
    correct the draft and retry; stop after a saved receipt.
    """
    # A failed attempt must not leave an earlier success as its receipt.
    context.receipt = None
    print("  [tool] send_email: validating and saving HTML (mock)", flush=True)
    try:
        draft = Newsletter.model_validate_json(newsletter_json)
        receipt = save_email(draft, context.evidence, context.settings)
    except ValueError as exc:
        return {"status": "error", "message": str(exc)}
    context.receipt = receipt
    return receipt
