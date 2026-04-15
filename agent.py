from __future__ import annotations
import os
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm, MultimodalAgent
from livekit.plugins import openai
from api import AssistantFnc
from prompts import WELCOME_MESSAGE, INSTRUCTIONS

load_dotenv()

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.SUBSCRIBE_ALL)
    await ctx.wait_for_participant()
    
    model = openai.realtime.RealtimeModel(
        instructions=INSTRUCTIONS,
        voice="shimmer",
        modalities=["audio", "text"]
    )
    
    assistant = MultimodalAgent(model=model, fnc_ctx=AssistantFnc())
    assistant.start(ctx.room)
    
    # Saludo inicial
    session = assistant.session
    session.conversation.item.create(
        llm.ChatMessage(role="assistant", content=WELCOME_MESSAGE)
    )
    session.response.create()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))