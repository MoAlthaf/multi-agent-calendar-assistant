from agents.scheduler_agent import scheduler_agent
from langchain_core.messages import HumanMessage

test_query="Schedule a team meeting titled 'Project Sync' for tomorrow from 10:00 AM to 11:00 AM"

response=scheduler_agent.invoke({
    "messages":[HumanMessage(content=test_query)]
    })
print(response["messages"][-1].content)