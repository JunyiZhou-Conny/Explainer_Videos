# @title Tools

def collect_evidence(result, evidence: Evidence) -> None:
    """Collect provider URL citations, never URLs extracted from model prose."""
    for message in result.messages:
        for content in message.contents:
            for citation in content.annotations or []:
                if getattr(citation.get("raw_representation"), "type", None) == "url_citation":
                    evidence.add(citation["url"], citation.get("title") or "")


def get_context(ctx: FunctionInvocationContext) -> NewsletterContext:
    """Read the application context passed through the Microsoft runtime."""
    context = ctx.kwargs.get("newsletter_context")
    if not isinstance(context, NewsletterContext):
        raise RuntimeError("This tool requires a NewsletterContext.")
    return context

async def invoke_agent(agent: Agent, prompt: str, context: NewsletterContext) -> str:
    """Run the orchestrator with a bounded tool loop."""
    result = await agent.run(
        prompt,
        function_invocation_kwargs={"newsletter_context": context},
    )
    return result.text or ""

@tool(approval_mode="never_require", description=send_newsletter.__doc__)
def send_email(ctx: FunctionInvocationContext) -> dict:
    return send_newsletter(get_context(ctx))
