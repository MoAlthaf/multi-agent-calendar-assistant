from agents.availability_checking_agent import availability_checking_agent


start_time="2026-05-26T10:00:00+03:00"
end_time="2026-05-29T11:00:00+03:00"

query=f"Check my availability from {start_time} to {end_time}."
response=availability_checking_agent.invoke({
    "messages":[{"role":"user","content":query}]
})
print(response["messages"][-1].content)