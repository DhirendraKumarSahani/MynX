from fastapi import APIRouter, HTTPException

from app.schemas.request_schema import ChatRequest
from app.schemas.response_schema import ChatGPTStyleResponse
from app.agents.react_agent import ReactAgentBuilder
from app.models.llm_model import LLMService
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from langchain_core.messages.utils import trim_messages
import json

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

            config = {
                "configurable": {
                    "thread_id": request.thread_id
                }
            }

            messages = [
                HumanMessage(content=request.query)
            ]

            trimmed_messages = trim_messages(
                messages,
                max_tokens=1500,
                strategy="last",
                token_counter=len
            )

            sent_text = ""

            for chunk in agent.agent.stream(
                {"messages": trimmed_messages},
                config=config
            ):

                if isinstance(chunk, dict) and "agent" in chunk:

                    agent_data = chunk["agent"]

                    if "messages" in agent_data:

                        msg = agent_data["messages"][-1]

                        if hasattr(msg, "content"):

                            new_text = msg.content

                            # prevent duplicate streaming
                            if new_text.startswith(sent_text):
                                token = new_text[len(sent_text):]
                            else:
                                token = new_text

                            sent_text = new_text

                            if token.strip():
                                yield f"data: {json.dumps({'token': token})}\n\n"

            # VERY IMPORTANT → end signal
            yield f"data: {json.dumps({'done': True})}\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
print("ROUTES MODULE LOADED")