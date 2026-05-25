from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from prompts.prompts import supervisor_prompt
from schemas.schemas import Route

from datetime import datetime

SUPERVISOR_SYSTEM_PROMPT = supervisor_prompt(datetime.now().strftime("%Y-%m-%d"))

def create_supervisor():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SUPERVISOR_SYSTEM_PROMPT),
        MessagesPlaceholder("messages"),
    ])

    return prompt | llm.with_structured_output(Route)
