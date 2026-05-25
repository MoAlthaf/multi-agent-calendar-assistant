from fastapi import APIRouter
from langchain_core.messages import AIMessage, HumanMessage

from graph.workflow import graph
from schemas.schemas import ChatRequest

router = APIRouter()


@router.post("/chat")
async def chat(req: ChatRequest):
    config = {"configurable": {"thread_id": req.thread_id}}
    response = await graph.ainvoke(
        {"messages": [HumanMessage(content=req.message)]},
        config=config,
    )

    for msg in reversed(response["messages"]):
        if isinstance(msg, AIMessage) and isinstance(msg.content, str) and msg.content.strip():
            return {"reply": msg.content}

    return {"reply": "I couldn't generate a response — please rephrase."}
