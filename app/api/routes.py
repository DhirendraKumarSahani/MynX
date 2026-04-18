from fastapi import APIRouter, HTTPException

from app.schemas.request_schema import ChatRequest
from app.schemas.response_schema import ChatGPTStyleResponse
from app.agents.react_agent import ReactAgentBuilder
from app.models.llm_model import LLMService
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.messages.utils import trim_messages
from langchain_core.messages.utils import count_tokens_approximately
import json
import traceback

router = APIRouter(prefix="/api/v1", tags=["AI Agent"])

# Singleton instances
agent_instance = None
llm_service = LLMService()


def get_agent():
    global agent_instance

    if agent_instance is None:
        agent_instance = ReactAgentBuilder()

    return agent_instance


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/chat", response_model=ChatGPTStyleResponse)
def chat(request: ChatRequest):

    try:

        agent = get_agent()

        # Run agent reasoning loop
        result = agent.run(
            query=request.query,
            thread_id=request.thread_id
        )

        final_message = result["messages"][-1].content

        # Create structured LLM
        structured_llm = llm_service.with_structured_output(
            ChatGPTStyleResponse
        )

        structured_response = structured_llm.invoke(final_message)

        return structured_response

    except Exception as e:

        raise HTTPException(status_code=500, detail=str(e))




@router.post("/chat/stream")
def chat_stream(request: ChatRequest):

    try:

        agent = get_agent()

        def event_stream():

            print("🚀 AGENT STREAM STARTED")

            config = {
                "configurable": {
                    "thread_id": request.thread_id
                }
            }

            # ==============================
            # STEP 1: Load memory
            # ==============================
            past_messages = agent.memory.get_messages(request.thread_id, limit=6) or []

            messages = []

            for role, content in past_messages:
                if role == "user":
                    messages.append(HumanMessage(content=content))
                else:
                    messages.append(AIMessage(content=content))

            # current user message
            messages.append(HumanMessage(content=request.query))
            

            messages = trim_messages(
                messages,
                max_tokens=2000,
                strategy="last",
                token_counter=count_tokens_approximately   # ✅ ADD THIS
            )

            # 🔥 SAFETY LIMIT (ADD HERE)
            if len(str(messages)) > 7000:
                messages = messages[-4:]

            # ==============================
            # STEP 2: Agent run
            # ==============================
            sent_text = ""

            for chunk in agent.agent.stream(
                {"messages": messages},
                config=config
            ):

                print("CHUNK:", chunk)

                msg = None

                if isinstance(chunk, dict):

                    if "messages" in chunk:
                        msg = chunk["messages"][-1]

                    elif "agent" in chunk and "messages" in chunk["agent"]:
                        msg = chunk["agent"]["messages"][-1]

                if msg and hasattr(msg, "content") and msg.content:

                    new_text = msg.content

                    if new_text.startswith(sent_text):
                        token = new_text[len(sent_text):]
                    else:
                        token = new_text

                    sent_text = new_text

                    if token.strip():
                        yield f"data: {json.dumps({'token': token})}\n\n"

            # ==============================
            # STEP 3: Save memory
            # ==============================
            if sent_text:
                agent.memory.save_message(request.thread_id, "user", request.query)
                agent.memory.save_message(request.thread_id, "ai", sent_text)

            # ==============================
            # STEP 4: End
            # ==============================
            yield f"data: {json.dumps({'done': True})}\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
print("ROUTES MODULE LOADED")
