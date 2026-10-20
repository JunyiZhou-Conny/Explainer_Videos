# @title Utils

# Sharded Settings
SCENARIO = "standard"  # Act 1 baseline.
CONTEXT_SCENARIO = "personalized"  # Same request for both modes in Act 2.
USE_FIXTURES = False  # Scripted responses in Acts 3–6 only; Acts 1–2 are live.
RUN_CONTEXT_EVALUATION = False  # Optional extra live calls at the end of Act 2.
CONTEXT_REPEATS = 3

# Evaluation lab: n different requests, each repeated m times.
EVAL_ACT = 6            # Choose 1–6; start with the complete agent system.
EVAL_N = 3              # First n applicable golden cases shown in the lab.
EVAL_M = 2              # Repeat each case m times (1–20).
EVAL_FIXTURES = True    # False = live model evaluation, with API usage.
EVAL_CONTEXT = "enriched"  # Act 2 only: "basic" or "enriched".

DB_PATH = Path("outputs/colab.sqlite")
OUTPUT_ROOT = Path("outputs/colab_artifacts")
MEMORY_PATH = Path("outputs/colab_memory.sqlite")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def ask_for_decision():
    while True:
        decision = input("Type approve or decline: ").strip().lower()
        if decision in {"approve", "decline"}:
            return decision
        print("Please enter approve or decline.")


async def review_order(ticket):
    print("\n👤 Manager review")
    print(customer_ask(ticket.request))
    print_cart(ticket.report)
    return ask_for_decision()


async def review_email(review):
    print("\n👤 Review this email draft")
    print(f"To: {review.draft.recipient}")
    print(f"Subject: {review.draft.subject}\n")
    print(review.draft.body)
    return ask_for_decision()


async def approve_review(review):
    print("TEST review decision: approve")
    return "approve"


async def decline_review(review):
    print("TEST review decision: decline")
    return "decline"
print(f"Model: {MODEL}")
print("scripted responses" if USE_FIXTURES else "live model")
