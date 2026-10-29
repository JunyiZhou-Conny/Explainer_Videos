# c5_error_event.py: module 4's runner loop without internet (as b6_module4.sh), printing each event's
# is_final_response(), content and error fields instead of reading content.parts.
import asyncio, os, sys, uuid
sys.path.insert(0, os.getcwd())
from google.genai import types
from app.runner import runner, session_service
async def main():
    sid, uid = str(uuid.uuid4()), str(uuid.uuid4())
    await session_service.create_session(app_name="production-agent", user_id=uid, session_id=sid, state={})
    msg = types.Content(role="user", parts=[types.Part(text="Hello!")])
    async for e in runner.runner.run_async(user_id=uid, session_id=sid, new_message=msg):
        print(f"event author={e.author} final={e.is_final_response()} content={e.content!r} "
              f"error_code={e.error_code!r} error_message={str(e.error_message)[:160]!r}")
asyncio.run(main())
