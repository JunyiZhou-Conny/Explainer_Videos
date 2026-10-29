# b6_sessions.py: module 4's AgentRunner.run (app/runner.py, unchanged), called twice the way two /chat requests
# call it, with the agent's model swapped for the stand-in: what does the model receive the second time?
import asyncio, os, sys
sys.path.insert(0, os.getcwd())                 # run from 4-production-ready/, like uvicorn app.main:app
from adk_standin import StandIn
from app.agent import agent
from app.runner import runner, session_service
print("agent model from the root .env:", agent.model)
agent.model = StandIn(answer=lambda si, contents: "(stand-in reply)")

async def main():
    for msg in ["My name is Sam.", "What is my name?"]:
        print(f"== POST /chat {{'user_message': {msg!r}}}")
        print("   response:", await runner.run(msg))
    sessions = await session_service.list_sessions(app_name="production-agent")
    print("sessions in the service:", len(sessions.sessions), "for users:",
          len({s.user_id for s in sessions.sessions}))
asyncio.run(main())
