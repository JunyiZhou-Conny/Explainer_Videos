# adk_standin.py: a stand-in for the Gemini model in ADK (google-adk 2.12.0), so ADK's own Runner, sessions,
# state, output_key and {key} substitution run for real without a key. StandIn is a BaseLlm whose replies are
# written here by hand ("(stand-in reply ...)"): they are not model output. For every call it prints what ADK
# would send to the model: the system instruction and the contents (roles and the start of each text).
import asyncio
import json
from typing import Callable

from google.adk.models import BaseLlm, LlmResponse
from google.genai import types


def short(text, n=110):
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[:n] + "…"


class StandIn(BaseLlm):
    model: str = "stand-in"
    answer: Callable = None          # answer(system_instruction, contents) -> reply text
    quiet: bool = False

    async def generate_content_async(self, llm_request, stream=False):
        si = llm_request.config.system_instruction if llm_request.config else None
        si = si if isinstance(si, str) else str(si)
        if not self.quiet:
            print(f"  [model call] system instruction: {short(si, 160)!r}")
            for c in llm_request.contents:
                for p in c.parts or []:
                    if p.text:
                        print(f"  [model call]   {c.role}: {short(p.text)!r}")
        cfg = llm_request.config
        schema = cfg and (cfg.response_schema or cfg.response_json_schema)
        if schema:
            print(f"  [model call] response schema sent with the request: {short(schema, 200)}; "
                  f"mime type {cfg.response_mime_type!r}")
        text = self.answer(si, llm_request.contents) if self.answer else "(stand-in reply)"
        yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text=text)]))


async def run(agent, message, app_name="checks", runner=None, user_id="student", session_id=None):
    """Runs one user message through a Runner; returns (runner, session)."""
    from google.adk.runners import InMemoryRunner
    runner = runner or InMemoryRunner(agent=agent, app_name=app_name)
    if session_id is None:
        session = await runner.session_service.create_session(app_name=app_name, user_id=user_id)
        session_id = session.id
    msg = types.Content(role="user", parts=[types.Part(text=message)])
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=msg):
        text = "".join(p.text or "" for p in (event.content.parts if event.content else []))
        print(f"  [event] author={event.author} final={event.is_final_response()} "
              f"state_delta={json.dumps(event.actions.state_delta)[:120]} text={short(text, 60)!r}")
    session = await runner.session_service.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
    return runner, session
