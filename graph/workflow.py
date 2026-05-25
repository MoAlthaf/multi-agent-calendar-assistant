import operator
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import AIMessage, BaseMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, StateGraph

from agents.scheduler_agent import scheduler_agent
from agents.availability_checking_agent import availability_checking_agent
from agents.editing_agent import editing_agent
from agents.removal_agent import removal_agent
from agents.supervisor_agent import create_supervisor


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_agent: str


supervisor = create_supervisor()


def supervisor_node(state: AgentState):
    route = supervisor.invoke({"messages": state["messages"]})
    update = {"next_agent": route.next_agent}
    if route.message:
        update["messages"] = [AIMessage(content=route.message)]
    return update


def router(state: AgentState):
    return state["next_agent"]


builder = StateGraph(AgentState)
builder.add_node("supervisor", supervisor_node)
builder.add_node("scheduler", scheduler_agent)
builder.add_node("availability", availability_checking_agent)
builder.add_node("editor", editing_agent)
builder.add_node("deleter",removal_agent)
builder.set_entry_point("supervisor")
builder.add_conditional_edges(
    "supervisor",
    router,
    {
        "scheduler": "scheduler",
        "availability": "availability",
        "editor":"editor",
        "deleter":"deleter",
        "chat": END,
        "FINISH": END,
    },
)
builder.add_edge("scheduler", "supervisor")
builder.add_edge("availability", "supervisor")
builder.add_edge("editor","supervisor")
builder.add_edge("deleter","supervisor")

graph = builder.compile(checkpointer=InMemorySaver())
